from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
student_auth = APIRouter()
class student(BaseModel):
    roll_number: str
    password: str
@student_auth.post("/student_auth")
def func_auth(candidate: student):
    if candidate.roll_number == "candidate" and candidate.password == "1234":
        return {
            "message": "Authentication successful"
        }
    raise HTTPException(status_code=401,detail="Authentication failed")