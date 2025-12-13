# backend/checkpointer.py
from sqlalchemy.orm import Session
from backend.models import Checkpoint, EventLog
import json

class Checkpointer:
    def __init__(self, db: Session):
        self.db = db

    def write_checkpoint(self, version_id: int, step_name: str, node_state: dict, iteration: int=0):
        cp = Checkpoint(version_id=version_id, step_name=step_name, node_state_json=node_state, iteration_count=iteration)
        self.db.add(cp)
        self.db.commit()
        self.db.refresh(cp)
        return cp

    def latest_checkpoint(self, version_id: int):
        return self.db.query(Checkpoint).filter_by(version_id=version_id).order_by(Checkpoint.created_at.desc()).first()

    def log_event(self, version_id: int, actor: str, action: str, payload: dict):
        ev = EventLog(version_id=version_id, actor=actor, action=action, payload=payload)
        self.db.add(ev)
        self.db.commit()
        return ev
