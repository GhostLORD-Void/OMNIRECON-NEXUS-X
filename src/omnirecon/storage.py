"""SQLite persistence for task plans."""
import sqlite3
from pathlib import Path
from omnirecon.schemas import TaskPlanResponse

class TaskStore:
    def __init__(self, database_path: str = "data/omnirecon.db") -> None:
        self.path = Path(database_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS tasks (task_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, payload TEXT NOT NULL)")

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def save(self, task: TaskPlanResponse) -> None:
        with self._connect() as db:
            db.execute("INSERT OR REPLACE INTO tasks VALUES (?, ?, ?)",
                       (str(task.task_id), task.created_at.isoformat(), task.model_dump_json()))

    def get(self, task_id: str) -> TaskPlanResponse | None:
        with self._connect() as db:
            row = db.execute("SELECT payload FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
        return TaskPlanResponse.model_validate_json(row["payload"]) if row else None

    def list(self, limit: int = 50) -> list[TaskPlanResponse]:
        with self._connect() as db:
            rows = db.execute("SELECT payload FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [TaskPlanResponse.model_validate_json(row["payload"]) for row in rows]
