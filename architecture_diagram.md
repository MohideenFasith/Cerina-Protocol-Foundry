# Architecture Diagram (textual)

Paste the following into a diagram tool (draw.io / Figma / Lucidchart) to create a visual diagram.

Boxes:
- Client: React Dashboard (WebSocket + REST)
- MCP Client (e.g., Claude Desktop) -> MCP Server Tool -> Backend
- FastAPI Backend
    - Supervisor Orchestrator (LangGraph runtime)
    - Worker Agents (Draftsmen x N)
    - Safety Guardian
    - Clinical Critic
    - Empathy Auditor
    - Checkpointer -> SQLite/Postgres (persistent)
    - Event Log
    - WebSocket PubSub (streams events to React)
- Database (SQLite/Postgres)

Arrows:
- React ↔ FastAPI (REST for commands, WebSocket for streaming)
- FastAPI ↔ LangGraph runtime (in-process or remote)
- LangGraph nodes ↔ Checkpointer (writes node state JSON)
- MCP Server ↔ FastAPI endpoints (wraps create/run)

Notes:
- Supervisor-Worker + Debate Swarm topology: multiple drafts created in parallel -> critics review -> debate thread -> supervisor decides -> halt_for_human when thresholds met.
- Checkpointing: every LangGraph node writes a Checkpoint row; resume reads latest checkpoint for that version.
