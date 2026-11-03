# OMNIRECON NEXUS X

A modular, security-conscious multi-agent platform foundation. The first milestone provides a typed FastAPI service, task planning, a small agent registry, health/status endpoints, and automated tests.

> Status: foundation / MVP scaffold. External model providers, live OSINT connectors, autonomous code execution, and production deployment are not enabled yet.

## Principles
- Human authorization and explicit scope for security-related work.
- No arbitrary shell execution or unrestricted tool access.
- Secrets are supplied through environment variables and never committed.
- Agents return structured results; unavailable integrations are reported rather than simulated.
- Tests and CI are part of the initial build.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn omnirecon.api:app --reload
```

Open http://127.0.0.1:8000/docs for the API docs.

## API
- `GET /health` — service health
- `GET /v1/agents` — registered agents and capabilities
- `POST /v1/tasks/plan` — create a transparent task plan

Example:
```bash
curl -X POST http://127.0.0.1:8000/v1/tasks/plan \
  -H "Content-Type: application/json" \
  -d '{"objective":"Review my web application security posture","authorized":true}'
```

The planning endpoint does not perform scans or contact external systems. Execution connectors will be added behind explicit permissions and per-tool scope checks.

## Configuration
See `.env.example`. Never commit real API keys or credentials.

## Development
```bash
pytest
ruff check .
```

## Roadmap
1. Foundation: API, typed models, agent registry, tests (current)
2. Model gateway: provider adapters, timeouts, budget controls
3. Agent orchestration: task state, delegation, retries, audit events
4. Approved tools: retrieval, web research, code review, scoped defensive security
5. Dashboard, observability, deployment hardening

## License
MIT
