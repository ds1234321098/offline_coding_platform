from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel, Field
from datetime import date, time, datetime
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
from Engine import session_maker
import sessions as ss
session = FastAPI()
class lab_session_class(BaseModel):
    branch: str
    semester: int
    session_date: date = Field(default_factory=date.today)
    session_time: time = Field(default_factory=lambda: datetime.now().time())
    status: str = "active"
@session.post("/create")
def create_session(lab_session: lab_session_class):
    Session=session_maker()
    try:
        new_session = ss.Sessions(
            branch=lab_session.branch,
            semester=lab_session.semester,
            session_date=lab_session.session_date,
            session_time=lab_session.session_time,
            status=lab_session.status
        )
        Session.add(new_session)
        Session.commit()
        Session.refresh(new_session)
        return {
            "message": "Session created successfully",
            "session.id": new_session.id,
            "session.branch": new_session.branch,
            "session.semester": new_session.semester,
            "session.session_date": new_session.session_date,
            "session.session_time": new_session.session_time,
            "session.status": new_session.status
        }
    except Exception as a:
        return {"error: ",a}
    finally:
        Session.close()
@session.get("/all")
def get_all_sessions():
    Session=session_maker()
    try:
        sessions=Session.query(ss.Sessions).all()
        return{
            "sessions": [
                {
                    "session.id": lab_session.id,
                    "session.branch": lab_session.branch,
                    "session.semester": lab_session.semester,
                    "session.date": lab_session.session_date,
                    "session.time": lab_session.session_time,
                    "session.status": lab_session.status
                }
                for lab_session in sessions
            ]
        }
    except Exception as a:
        return("error: ",a)
    finally:
        Session.close()
@session.get("/{session_id}")
def get_session(session_id: str):
    Session=session_maker()
    try:
        sessions=Session.query(ss.Sessions).all()
        for session in sessions:
            if session.id == session_id:
                return{
                    "message": "successfully found the session",
                    "session.id": session.id,
                    "session.branch": session.branch,
                    "session.semester": session.semester,
                    "session.session_date": session.session_date,
                    "session.session_time": session.session_time
                }
        raise HTTPException(status_code=404,detail="Session not found")
    except Exception as a:
        return{"error: ",a}
    finally:
        Session.close()
@session.put("/end")
def end_session(session_id: str):
    Session=session_maker()
    try:
        sessions=Session.query(ss.Sessions).filter(ss.Sessions.id==session_id).all()
        if len(sessions) == 0:
            return {"message":"session not found"}
        if sessions[0].status=='active':
            sessions[0].status='ended'
            Session.commit()
            return {
                "id":sessions[0].id,
                "branch":sessions[0].branch,
                "semester":sessions[0].semester,
                "session_date":sessions[0].session_date,
                "session_time":sessions[0].session_time,
                "status":sessions[0].status
            }
        raise HTTPException(status_code=404,detail="Session not found")
    except Exception as a:
        return{"error: ",a}
    finally:
        Session.close()