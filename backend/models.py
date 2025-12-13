# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    intent_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    current_version_id = Column(Integer, ForeignKey("versions.id"), nullable=True)

class Version(Base):
    __tablename__ = "versions"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    version_number = Column(Integer, default=1)
    status = Column(String, default="draft")  # draft, halted, approved, finalized
    created_at = Column(DateTime, default=datetime.utcnow)

class Draft(Base):
    __tablename__ = "drafts"
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey("versions.id"))
    agent_name = Column(String)
    content = Column(Text)
    score_json = Column(JSON)  # e.g. {"safety":0.9,"empathy":0.7,"clinical":0.85}
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentNote(Base):
    __tablename__ = "agent_notes"
    id = Column(Integer, primary_key=True)
    draft_id = Column(Integer, ForeignKey("drafts.id"), nullable=True)
    agent_name = Column(String)
    note_type = Column(String)
    content = Column(Text)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Checkpoint(Base):
    __tablename__ = "checkpoints"
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey("versions.id"))
    step_name = Column(String)
    node_state_json = Column(JSON)
    iteration_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class EventLog(Base):
    __tablename__ = "event_log"
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey("versions.id"))
    actor = Column(String)
    action = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
