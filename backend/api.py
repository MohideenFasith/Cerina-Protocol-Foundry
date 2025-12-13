from fastapi import FastAPI, WebSocket, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from backend.models import Base, Project, Version, Draft
from backend.langgraph_workflow import CerinaFoundryGraph
from backend.checkpointer import Checkpointer


from backend.models import Base, Project, Version, Draft
from backend.langgraph_workflow import CerinaFoundryGraph
from backend.checkpointer import Checkpointer

# -------------------------------------------------------------------
# Database setup
# -------------------------------------------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./cerina.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------
# FastAPI app
# -------------------------------------------------------------------

app = FastAPI(title="Cerina Protocol Foundry API")

# -------------------------------------------------------------------
# CORS (CRITICAL FOR FRONTEND)
# -------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# API endpoints
# -------------------------------------------------------------------

@app.post("/api/projects/")
def create_project(payload: dict):
    """
    Create a new project + initial version
    """
    db = SessionLocal()

    intent = payload.get("intent")
    if not intent:
        raise HTTPException(status_code=400, detail="intent is required")

    project = Project(
        user_id=payload.get("user_id", "guest"),
        intent_text=intent,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    version = Version(
        project_id=project.id,
        version_number=1,
        status="draft",
    )
    db.add(version)
    db.commit()
    db.refresh(version)

    project.current_version_id = version.id
    db.add(project)
    db.commit()

    return {
        "project_id": project.id,
        "version_id": version.id,
        "status": "created",
    }


@app.post("/api/projects/{project_id}/run")
def run_project(
    project_id: int,
    payload: dict,
    background_tasks: BackgroundTasks,
):
    """
    Run the LangGraph workflow in the background
    """
    db = SessionLocal()

    project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    version = db.query(Version).get(project.current_version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    graph = CerinaFoundryGraph(db)

    background_tasks.add_task(
        graph.run,
        project_id,
        version.id,
        project.intent_text,
        payload.get("halt_for_human", True),
    )

    return {
        "project_id": project_id,
        "version_id": version.id,
        "status": "running",
    }


@app.post("/api/projects/{project_id}/versions/{version_id}/approve")
def approve_version(project_id: int, version_id: int, payload: dict):
    """
    Human-in-the-loop approval endpoint
    """
    db = SessionLocal()

    content = payload.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="content is required")

    draft = Draft(
        version_id=version_id,
        agent_name="human_editor",
        content=content,
        score_json={},
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)

    checkpointer = Checkpointer(db)
    checkpointer.write_checkpoint(
        version_id,
        "human_approved",
        {
            "human_draft_id": draft.id,
            "content": content,
        },
    )
    checkpointer.log_event(
        version_id,
        "human",
        "approved",
        {"draft_id": draft.id},
    )

    return {
        "status": "approved",
        "version_id": version_id,
        "draft_id": draft.id,
    }


# -------------------------------------------------------------------
# WebSocket (demo / future streaming)
# -------------------------------------------------------------------

@app.websocket("/ws/projects/{project_id}/versions/{version_id}")
async def project_ws(websocket: WebSocket, project_id: int, version_id: int):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            await websocket.send_text(f"pong: {msg}")
    except Exception:
        await websocket.close()
