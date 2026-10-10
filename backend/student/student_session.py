import os,sys
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
import Engine
from student_enteries_in_session import Student_Enteries
from students import Students
from sessions import Sessions
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
session=sessionmaker(bind=Engine.engine)
Session=session()
student_session=FastAPI()
class Student_Response(BaseModel):
    id:str
    roll_number:str
@student_session.post("/create")
def create_entry(entry:Student_Response):
    sessions=Session.query(Sessions).filter_by(id=entry.id).all()
    if len(sessions) is 0:
        raise HTTPException(status_code=404,detail="session not found")
    students=Session.query(Students).filter_by(roll_number=entry.roll_number).all()
    if len(students) is 0:
        raise HTTPException(status_code=404,detail="student not found")
    entries=Session.query(Student_Enteries).filter(and_(Student_Enteries.id==entry.id,Student_Enteries.roll_number==entry.roll_number)).all()
    if len(entries) is not 0:
        return {"message":"student already in session"}
    s1=Student_Enteries(id=entry.id,roll_number=entry.roll_number)
    Session.add(s1)
    Session.commit()
@student_session.put("/leave")
def leave_entry(entry:Student_Response):
    sessions=Session.query(Sessions).filter_by(id=entry.id).all()
    if len(sessions) is 0:
        raise HTTPException(status_code=404,detail="session not found")
    students=Session.query(Students).filter_by(roll_number=entry.roll_number).all()
    if len(students) is 0:
        raise HTTPException(status_code=404,detail="student not found")
    entries=Session.query(Student_Enteries).filter(and_(Student_Enteries.id==entry.id,Student_Enteries.roll_number==entry.roll_number)).all()
    if len(entries) is 0:
        return {"message":"student not registered in session"}
    entries[0].status='Left'
    Session.commit()
    return {"message":"successfully left the session"}