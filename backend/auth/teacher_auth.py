from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
from verify_password import verify_entered_password
from engine import session_maker
import teachers as tc
teacher_auth = FastAPI()
class Teacher(BaseModel):
    username: str
    password: str
@teacher_auth.post("/teacher_auth")
def func_auth(teacher: Teacher):
    Session=session_maker()
    try:
        data=Session.query(tc.Teachers).filter_by(username=teacher.username).all()
        if len(data) is not 0:
            if teacher.username == data[0].username and verify_entered_password(teacher.password,data[0].password_hash):
                return{
                    "message": "Authentication successful"
                }
        raise HTTPException(status_code=401,detail="Authentication failed")
    except Exception as a:
        return {"error ":a}
    finally:
        Session.close()