from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
from sqlalchemy.orm import sessionmaker
from verify_password import verify_entered_password
import Engine
import teachers as tc
session=sessionmaker(bind=Engine.engine)
Session=session()
teacher_auth = APIRouter()
class Teacher(BaseModel):
    username: str
    password: str
@teacher_auth.post("/teacher_auth")
def func_auth(teacher: Teacher):
    data=Session.query(tc.Teachers).filter_by(username=teacher.username).all()
    if len(data) is not 0:
        if teacher.username == data[0].username and verify_entered_password(teacher.password,data[0].password_hash):
            return{
                "message": "Authentication successful"
            }
    raise HTTPException(status_code=401,detail="Authentication failed")