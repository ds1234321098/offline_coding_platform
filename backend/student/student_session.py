import os, sys
from sqlalchemy import and_
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database_queries")))
from Engine import session_maker
from student_enteries_in_session import Student_Enteries
from students import Students
from sessions import Sessions
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
student_session = APIRouter()
class Student_Response(BaseModel):
    id: str
    roll_number: str
@student_session.post("/create")
def create_entry(entry: Student_Response):
    Session = session_maker()
    try:
        sessions = Session.query(Sessions).filter_by(id=entry.id).first()
        if sessions is None:
            raise HTTPException(status_code=404,detail="Session not found")
        if sessions.status != "active":
            raise HTTPException(status_code=400,detail="Cannot join an ended session")
        students = Session.query(Students).filter_by(roll_number=entry.roll_number).first()
        if students is None:
            raise HTTPException(status_code=404,detail="Student not found")
        entries = Session.query(Student_Enteries).filter(and_(Student_Enteries.id == entry.id,Student_Enteries.roll_number == entry.roll_number)).first()
        if entries is not None:
            if entries.status == "Present":
                return {
                    "message": "Student already in session",
                    "id": entry.id,
                    "roll_number": entry.roll_number,
                    "status": entries.status
                }
            entries.status = "Present"
            Session.commit()
            return {
                "message": "Student rejoined successfully",
                "id": entry.id,
                "roll_number": entry.roll_number,
                "status": entries.status
            }
        s1 = Student_Enteries(id=entry.id,roll_number=entry.roll_number,status="Present")
        Session.add(s1)
        Session.commit()
        return {
            "message": "Student joined successfully",
            "id": entry.id,
            "roll_number": entry.roll_number,
            "status": s1.status
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        print(f"Error joining session: {a}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    finally:
        Session.close()
@student_session.put("/leave")
def leave_entry(entry: Student_Response):
    Session = session_maker()
    try:
        sessions = Session.query(Sessions).filter_by(id=entry.id).first()
        if sessions is None:
            raise HTTPException(status_code=404,detail="Session not found")
        students = Session.query(Students).filter_by(roll_number=entry.roll_number).first()
        if students is None:
            raise HTTPException(status_code=404,detail="Student not found")
        entries = Session.query(Student_Enteries).filter(and_(Student_Enteries.id == entry.id,Student_Enteries.roll_number == entry.roll_number)).first()
        if entries is None:
            raise HTTPException(status_code=404,detail="Student is not registered in this session")
        if entries.status == "Left":
            return {
                "message": "Student has already left the session",
                "id": entry.id,
                "roll_number": entry.roll_number,
                "status": entries.status
            }
        entries.status = "Left"
        Session.commit()
        return {
            "message": "Student left the session successfully",
            "id": entry.id,
            "roll_number": entry.roll_number,
            "status": entries.status
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        print(f"Error leaving session: {a}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    finally:
        Session.close()