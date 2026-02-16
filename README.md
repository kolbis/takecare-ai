# TakeCare — AI-Powered Medication Assistant (WhatsApp)

Help older adults take medications correctly and safely via WhatsApp.

## Structure

- **api/** — FastAPI: webhooks, REST, scheduler, caregiver notifications
- **app/** — Application logic (DDD): use cases, domain, repositories (mocked), RAG
- **agentic/** — LangGraph + agents: graph, tools, skills, prompts
- **shared/** — Shared types, i18n (EN/HE)

## Setup

```bash
uv sync
```

Run API:

```bash
uv run --project api uvicorn api.main:app --reload
```

Run from a specific package:

```bash
uv run --project agentic python -c "from agentic.graph.graph import graph; print(graph)"
```
