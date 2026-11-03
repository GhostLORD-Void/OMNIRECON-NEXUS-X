from omnirecon.schemas import PlannedStep, TaskPlanResponse
from omnirecon.storage import TaskStore

def test_task_store_round_trip(tmp_path):
    store = TaskStore(str(tmp_path / "tasks.db"))
    task = TaskPlanResponse(objective="Test persistence safely", authorized=False,
        steps=[PlannedStep(agent="coordinator", action="Plan", rationale="Test")], execution_note="Plan only")
    store.save(task)
    assert store.get(str(task.task_id)) == task
    assert store.list()[0].task_id == task.task_id
