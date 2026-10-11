from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel, Field
from datetime import date, time, datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database_queries")))
from Engine import session_maker
import sessions as ss
session = FastAPI()
class lab_session_class(BaseModel):
    branch: str
    semester: int
    session_date: date = Field(default_factory=date.today)
    session_time: time = Field(default_factory=lambda: datetime.now().time())
@session.post("/create")
def create_session(lab_session: lab_session_class):
    Session = session_maker()
    try:
        new_session = ss.Sessions(branch=lab_session.branch,semester=lab_session.semester,session_date=lab_session.session_date,session_time=lab_session.session_time,status="active")
        Session.add(new_session)
        Session.commit()
        Session.refresh(new_session)
        return {
            "message": "Session created successfully",
            "id": new_session.id,
            "branch": new_session.branch,
            "semester": new_session.semester,
            "session_date": new_session.session_date,
            "session_time": new_session.session_time,
            "status": new_session.status
        }
    except Exception as a:
        Session.rollback()
        print(f"Error creating session: {a}")
        raise HTTPException(status_code=500,detail="Failed to create session")
    finally:
        Session.close()
@session.get("/all")
def get_all_sessions():
    Session = session_maker()
    try:
        sessions = Session.query(ss.Sessions).all()
        return {
            "sessions": [
                {
                    "id": lab_session.id,
                    "branch": lab_session.branch,
                    "semester": lab_session.semester,
                    "session_date": lab_session.session_date,
                    "session_time": lab_session.session_time,
                    "status": lab_session.status
                }
                for lab_session in sessions
            ]
        }
    except Exception as a:
        print(f"Error retrieving sessions: {a}")
        raise HTTPException(status_code=500,detail="Failed to retrieve sessions")
    finally:
        Session.close()
@session.get("/{session_id}")
def get_session(session_id: str):
    Session = session_maker()
    try:
        sessions = Session.query(ss.Sessions).filter(ss.Sessions.id == session_id).first()
        if sessions is None:
            raise HTTPException(status_code=404,detail="Session not found")
        return {
            "message": "Successfully found the session",
            "id": sessions.id,
            "branch": sessions.branch,
            "semester": sessions.semester,
            "session_date": sessions.session_date,
            "session_time": sessions.session_time,
            "status": sessions.status
        }
    except HTTPException:
        raise
    except Exception as a:
        print(f"Error retrieving session: {a}")
        raise HTTPException(status_code=500,detail="Internal server error")
    finally:
        Session.close()
@session.put("/end")
def end_session(session_id: str):
    Session = session_maker()
    try:
        sessions = Session.query(ss.Sessions).filter(ss.Sessions.id == session_id).first()
        if sessions is None:
            raise HTTPException(status_code=404,detail="Session not found")
        if sessions.status == "ended":
            return {
                "message": "Session has already ended",
                "id": sessions.id,
                "status": sessions.status
            }
        sessions.status = "ended"
        Session.commit()
        return {
            "message": "Session ended successfully",
            "id": sessions.id,
            "branch": sessions.branch,
            "semester": sessions.semester,
            "session_date": sessions.session_date,
            "session_time": sessions.session_time,
            "status": sessions.status
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        print(f"Error ending session: {a}")
        raise HTTPException(status_code=500,detail="Internal server error")
    finally:
        Session.close()