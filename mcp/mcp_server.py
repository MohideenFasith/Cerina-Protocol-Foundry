# mcp/mcp_server.py
# Skeleton MCP tool server. Replace pseudocode with your mcp-python usage/config.
from fastapi import FastAPI
from backend.api import create_project, run_project
app = FastAPI(title="Cerina MCP Wrapper (skeleton)")

@app.post('/mcp/cerina_create_protocol')
async def cerina_create_protocol(payload: dict):
    # payload: {intent: str, halt_for_human: bool}
    project = create_project({"intent": payload.get("intent",""), "user_id": payload.get("user_id","mcp_client")})
    run_project(project_id=project['project_id'], payload={"halt_for_human": payload.get('halt_for_human', True)})
    return {"status": "accepted", "project_id": project['project_id'], "version_id": project['version_id']}
