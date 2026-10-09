from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel, Field
from datetime import date, time, datetime
import uuid
import os,sys
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
import Engine
import sessions as ss
engine_session=sessionmaker(bind=Engine.engine)
Session=engine_session()
session = FastAPI()
class lab_session_class(BaseModel):
    branch: str
    semester: int
    session_date: date = Field(default_factory=date.today)
    session_time: time = Field(default_factory=lambda: datetime.now().time())
    status: str = "active"
@session.post("/create")
def create_session(lab_session: lab_session_class):
    new_session=ss.Sessions(id=uuid.uuid4(),branch=lab_session.branch,semester=lab_session.semester,session_date=lab_session.session_date,session_time=lab_session.session_time,status=lab_session.status)
    Session.add(new_session)
    Session.commit()
    return{
        "message": "Session created successfully",
        "session.id": new_session.id,
        "session.branch": new_session.branch,
        "session.semester": new_session.semester,
        "session.session_date": new_session.session_date,
        "session.session_time": new_session.session_time,
        "session.status": new_session.status
    }
@session.get("/all")
def get_all_sessions():
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
@session.get("/{session_id}")
def get_session(session_id: uuid.UUID):
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
@session.put("/end")
def end_session(session_id: uuid.UUID):
    sessions=Session.query(ss.Sessions).all()
    for lab_session in sessions:
        if lab_session.id == session_id:
            (Session.query(ss.Sessions).filter_by(id=session_id).all())[0].status="ended"
            Session.commit()
            return{
                "message": "Session ended successfully",
                "session.id": (Session.query(ss.Sessions).filter_by(id=session_id).all())[0].id,
                "session.branch": (Session.query(ss.Sessions).filter_by(id=session_id).all())[0].branch,
                "session.semester": (Session.query(ss.Sessions).filter_by(id=session_id).all())[0].semester,
                "session.date": (Session.query(ss.Sessions).filter_by(id=session_id).all())[0].session_date,
                "session.time": (Session.query(ss.Sessions).filter_by(id=session_id).all())[0].session_time,
                "session.status": (Session.query(ss.Sessions).filter_by(id=session_id).all())[0].status
            }
    raise HTTPException(status_code=404,detail="Session not found")