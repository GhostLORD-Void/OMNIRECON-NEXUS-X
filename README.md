# OMNIRECON NEXUS X

A modular, security-conscious multi-agent platform. Current release: **0.2.0 foundation**.

## Included
- FastAPI service with OpenAPI docs
- Agent catalogue and deterministic task planner
- SQLite persistence for task plans
- Small browser dashboard at `/dashboard`
- Optional OpenAI-compatible chat endpoint
- Central tool permission policy (tools remain disabled until an adapter is deliberately enabled)
- Automated tests and GitHub Actions CI

## Quick start
Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn omnirecon.api:app --reload
```

Visit `http://127.0.0.1:8000/dashboard` or `/docs`.

## API
- `GET /health`
- `GET /v1/agents`
- `POST /v1/tasks/plan`
- `GET /v1/tasks?limit=20`
- `GET /v1/tasks/{task_id}`
- `POST /v1/chat` (requires provider configuration)

Example task plan:
```bash
curl -X POST http://127.0.0.1:8000/v1/tasks/plan \
  -H "Content-Type: application/json" \
  -d '{"objective":"Review my web application security posture","authorized":true}'
```

## Model provider
Set these environment variables to use an OpenAI-compatible endpoint:
- `MODEL_BASE_URL` — HTTPS endpoint base, for example your provider's API base URL
- `MODEL_API_KEY` — secret API key; never commit it
- `MODEL_NAME` — provider model identifier
- `MODEL_TIMEOUT_SECONDS` — request timeout (default 45)

The chat adapter sends only the supplied prompt to the configured provider. It does not expose local tools or execute generated code.

## Security boundaries
- Task planning is not task execution.
- No arbitrary shell, filesystem, scanning, or browser automation is enabled.
- Defensive security work must be explicitly authorized and scoped.
- Provider credentials belong in environment variables or a secret manager.
- Configure HTTPS for production and place the service behind authentication before exposing it publicly.

## Tests
```bash
pytest
ruff check .
```

## Roadmap
1. Foundation, task planning, persistence, API, dashboard (implemented)
2. Provider adapters and model gateway (initial OpenAI-compatible adapter implemented)
3. Durable orchestration, event/audit log, cancellation and retries
4. Scoped, permission-gated integrations
5. Authentication, RBAC, deployment and operational hardening

## License
MIT
