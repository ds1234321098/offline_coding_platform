from pydantic import BaseModel
import sys
import os
from password_hash import hash_password
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
from Engine import session_maker
import teachers as tc
class teacher_class(BaseModel):
    name: str
    username: str
    password: str
def add(candidate: teacher_class):
    Session=session_maker()
    try:    
        teachers=Session.query(tc.Teachers).filter(tc.Teachers.username==candidate.username).all()
        if len(teachers)!=0:
            return False
        new_teacher=tc.Teachers(username=candidate.username,name=candidate.name,password_hash=hash_password(candidate.password))
        Session.add(new_teacher)
        Session.commit()
        return True
    except Exception as a:
        Session.rollback()
        print(f"error: {a}")
        return False
    finally:
        Session.close()
def read(username: str):
    Session=session_maker()
    try:
        teachers=Session.query(tc.Teachers).filter(tc.Teachers.username==username).all()
        if len(teachers)==0:
            return None
        return teachers[0]
    except Exception as a:
        print(f"error: {a}")
        return None
    finally:
        Session.close()
def update(username: str, candidate: teacher_class):
    Session=session_maker()
    try:
        teachers=Session.query(tc.Teachers).filter(tc.Teachers.username==username).all()
        if len(teachers)==0:
            return False
        teachers[0].name=candidate.name
        teachers[0].password_hash=hash_password(candidate.password)
        Session.commit()
        return True
    except Exception as a:
        Session.rollback()
        print(f"error is : {a}")
        return False
    finally:
        Session.close()
def delete(username: str):
    Session=session_maker()
    try:
        teachers=Session.query(tc.Teachers).filter(tc.Teachers.username==username).all()
        if len(teachers)==0:
            return False
        Session.delete(teachers[0])
        Session.commit()
        return True
    except Exception as a:
        Session.rollback()
        print(f"error: {a}")
        return False
    finally:
        Session.close()
def get_all():
    Session=session_maker()
    try:
        teachers=Session.query(tc.Teachers).all()
        return teachers
    except Exception as a:
        print(f"error: {a}")
        return []
    finally:
        Session.close()