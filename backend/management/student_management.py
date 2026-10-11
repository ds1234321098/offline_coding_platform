from pydantic import BaseModel
import sys
from password_hash import hash_password
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
from Engine import session_maker
import students as st
class student_class(BaseModel):
    name: str
    roll_number: str
    semester: int
    branch: str
    password: str
def add(candidate: student_class):
    Session=session_maker()
    try:
        students=Session.query(st.Students).filter(st.Students.roll_number==candidate.roll_number).all()
        if len(students) != 0:
            return False
        new_Student=st.Students(roll_number=candidate.roll_number,name=candidate.name,semester=candidate.semester,branch=candidate.branch,password_hash=hash_password(candidate.password))
        Session.add(new_Student)
        Session.commit()
        return True
    except Exception as a:
        Session.rollback()
        print(f"error: {a}")
        return False
    finally:
        Session.close()
def read(roll_number: str):
    Session=session_maker()
    try:
        students=Session.query(st.Students).filter(st.Students.roll_number==roll_number).all()
        if len(students)==0:
            return None
        return students[0]
    except Exception as a:
        print(f"error: {a}")
        return None
    finally:
        Session.close()
def update(roll_number: str, candidate: student_class):
    Session=session_maker()
    try:
        students=Session.query(st.Students).filter(st.Students.roll_number==roll_number).all()
        if len(students) == 0:
            return False
        students[0].name=candidate.name
        students[0].branch=candidate.branch
        students[0].semester=candidate.semester
        students[0].password_hash=hash_password(candidate.password)
        Session.commit()
        return True
    except Exception as a:
        Session.rollback()
        print(f"error: {a}")
        return False
    finally:
        Session.close()
def delete(roll_number: str):
    Session=session_maker()
    try:
        students=Session.query(st.Students).filter(st.Students.roll_number==roll_number).all()
        if len(students) == 0:
            return False
        Session.delete(students[0])
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
        students=Session.query(st.Students).all()
        return students
    except Exception as a:
        print(f"error: {a}")
        return []
    finally:
        Session.close()