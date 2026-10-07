from pydantic import BaseModel
import sys
from password_hash import hash_password
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
from sqlalchemy.orm import sessionmaker
import Engine
import students as st
session=sessionmaker(bind=Engine.engine)
Session=session()
students=[]
class student_class(BaseModel):
    name: str
    roll_number: str
    semester: int
    branch: str
    password: str
def add(candidate: student_class):
    students=Session.query(st.Students).all()
    for a in students:
        if a.roll_number == candidate.roll_number:
            return False
    new_Student=st.Students(roll_number=candidate.roll_number,name=candidate.name,semester=candidate.semester,branch=candidate.branch,password_hash=hash_password(candidate.password))
    Session.add(new_Student)
    Session.commit()
    return True
def read(roll_number: str):
    for a in students:
        if a.roll_number == roll_number:
            return a
    return None
def update(roll_number: str, candidate: student_class):
    for i in range(len(students)):
        if students[i].roll_number == roll_number:
            students[i] = candidate
            return True
    return False
def delete(roll_number: str):
    for i in range(len(students)):
        if students[i].roll_number == roll_number:
            students.pop(i)
            return True
    return False
def get_all():
    return students
Session.close()