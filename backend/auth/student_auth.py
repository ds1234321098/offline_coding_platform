from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os,sys
from verify_password import verify_entered_password
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
import Engine
import students as st
session=sessionmaker(Engine.engine)
Session=session()
student_auth = APIRouter()
class student(BaseModel):
    roll_number: str
    password: str
@student_auth.post("/student_auth")
def func_auth(candidate: student):
    data=Session.query(st.Students).filter_by(roll_number=candidate.roll_number).all()
    if len(data) is not 0:
        if candidate.roll_number == data[0].roll_number and verify_entered_password(candidate.password,data[0].password_hash):
            return {
                "message": "Authentication successful"
            }
    raise HTTPException(status_code=401,detail="Authentication failed")