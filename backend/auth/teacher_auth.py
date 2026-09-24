from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
teacher_auth = APIRouter()
class Teacher(BaseModel):
    username: str
    password: str
@teacher_auth.post("/teacher_auth")
def func_auth(teacher: Teacher):
    if teacher.username == "teacher" and teacher.password == "1234":
        return{
            "message": "Authentication successful"
        }
    raise HTTPException(status_code=401,detail="Authentication failed")