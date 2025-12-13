# Cerina Protocol Foundry - Sprint Deliverable (Starter Repo)

This repository contains a focused, runnable starter implementation for the "Cerina Protocol Foundry" multi-agent system.
It provides a Python backend skeleton (FastAPI + SQLAlchemy + LangGraph-like workflow), an MCP tool wrapper skeleton,
and a minimal React frontend skeleton demonstrating the Human-in-the-Loop halt/approve flow.

## What's included
- `backend/` : FastAPI server, DB models (SQLite via SQLAlchemy), checkpointer, LangGraph workflow skeleton
- `mcp/` : MCP tool skeleton wrapping the backend
- `frontend/` : React + TypeScript minimal app skeleton (App.tsx) to connect via WebSocket and REST
- `architecture_diagram.md` : Textual architecture diagram and instructions to create visuals
- `loom_instructions.txt` : What to record in the Loom demo (max 5 minutes)
- `requirements.txt` : Python dependencies (starter)

## How to run (development)
1. Create Python venv and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start FastAPI backend:
   ```bash
   uvicorn backend.api:app --reload --port 8000
   ```
3. Frontend: open `frontend/` and run standard React setup (this is a skeleton; adapt as needed).

## Notes
- This repo is a starting point and intentionally minimal so it can be iterated rapidly.
- Replace the LangGraph pseudocode with your concrete LangGraph nodes and LLM adapters.
- MCP server uses skeleton code; register and run using your mcp-python config as needed.
