# OMNIRECON NEXUS X

A local-first, modular multi-agent AI platform. Current development target: **MAXPOWER hybrid mode**.

## Implemented foundation
- FastAPI API and OpenAPI docs
- Coordinator, research, engineering, defense and analytics agent catalogue
- Sequential multi-agent reasoning endpoint with final synthesis
- Hybrid model gateway: OpenAI, Anthropic, Google Gemini and local OpenAI-compatible endpoints
- Ordered fallback across configured providers
- SQLite task-plan persistence
- Browser dashboard at `/dashboard`
- Central permission policy, tests, CI workflow and Docker support

## Local setup
Python 3.11+:

```bash
git clone https://github.com/GhostLORD-Void/OMNIRECON-NEXUS-X.git
cd OMNIRECON-NEXUS-X
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env and add credentials for at least one provider.
uvicorn omnirecon.api:app --reload
```

Dashboard: `http://127.0.0.1:8000/dashboard`  
API docs: `http://127.0.0.1:8000/docs`

## Configure hybrid models
Edit only your local `.env`. Never commit API keys.
- `PROVIDER_ORDER=openai,anthropic,google,local` defines fallback priority.
- Configure one or more providers. The router uses the first configured provider and falls back on request failure.
- For local Ollama OpenAI-compatible API, set `LOCAL_MODEL_BASE_URL=http://127.0.0.1:11434/v1`, `LOCAL_MODEL_NAME` to a model installed locally, and `LOCAL_MODEL_API_KEY=local`.

The application does not download models or create provider accounts. API usage may incur provider charges.

## API
- `GET /health`
- `GET /v1/agents`
- `GET /v1/providers` — configured provider names/models only; no secrets
- `POST /v1/chat` — single model response
- `POST /v1/agents/run` — coordinator, specialist analysis and synthesis
- `POST /v1/tasks/plan`
- `GET /v1/tasks?limit=20`
- `GET /v1/tasks/{task_id}`

Example multi-agent request:

```bash
curl -X POST http://127.0.0.1:8000/v1/agents/run \
  -H "Content-Type: application/json" \
  -d '{"objective":"Design a secure backup strategy for my application","authorized":true}'
```

## Execution and security boundaries
MAXPOWER hybrid mode currently means multi-agent model reasoning, not unrestricted autonomous action. The runtime does not execute shell commands, run scans, modify files, or invoke external tools. Tool integrations must be separately implemented, scoped, logged, and gated by explicit approval. Protect the local API before exposing it beyond localhost.

## Validation
```bash
pytest
ruff check .
```

## Roadmap
- [x] Multi-provider gateway and fallback
- [x] Sequential agent-team reasoning
- [x] Local-first configuration
- [ ] Authenticated user sessions and role-based access
- [ ] Persistent agent-run history and audit events
- [ ] Human approval queue and scoped tool adapters
- [ ] Dashboard task submission and streaming progress

MIT License.
