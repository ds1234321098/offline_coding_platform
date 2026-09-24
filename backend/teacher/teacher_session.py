from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import date, time, datetime
import uuid
session = APIRouter()
sessions = []
class lab_session_class(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    branch: str
    semester: int
    session_date: date = Field(default_factory=date.today)
    session_time: time = Field(default_factory=lambda: datetime.now().time())
    status: str = "active"
@session.post("/create")
def create_session(lab_session: lab_session_class):
    sessions.append(lab_session)
    return{
        "message": "Session created successfully",
        "session": lab_session
    }
@session.get("/all")
def get_all_sessions():
    return{
        "sessions": sessions
    }
@session.get("/{session_id}")
def get_session(session_id: str):
    for lab_session in sessions:
        if lab_session.id == session_id:
            return{
                "session": lab_session
            }
    raise HTTPException(status_code=404,detail="Session not found")
@session.put("/end")
def end_session(session_id: str):
    for lab_session in sessions:
        if lab_session.id == session_id:
            lab_session.status = "ended"
            return{
                "message": "Session ended successfully",
                "session": lab_session
            }
    raise HTTPException(status_code=404,detail="Session not found")