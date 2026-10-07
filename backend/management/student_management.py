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
    students=Session.query(st.Students).all()
    for a in students:
        if a.roll_number == roll_number:
            return a
    return None
def update(roll_number: str, candidate: student_class):
    try:
        students=Session.query(st.Students).all()
        with Session.begin_nested():
            for person in students:
                if person.roll_number == roll_number:
                    (Session.query(st.Students).filter_by(roll_number=roll_number).all())[0].name=candidate.name
                    (Session.query(st.Students).filter_by(roll_number=roll_number).all())[0].branch=candidate.branch
                    (Session.query(st.Students).filter_by(roll_number=roll_number).all())[0].semester=candidate.semester
                    (Session.query(st.Students).filter_by(roll_number=roll_number).all())[0].password_hash=hash_password(candidate.password)
                    Session.commit()
                    return True
            return False
    except Exception as a:
        print(f"Error : {a}")
def delete(roll_number: str):
    students=Session.query(st.Students).all()
    for person in students:
        if person.roll_number==roll_number:
            Session.delete(person)
            Session.commit()
            return True
    return False
def get_all():
    students=Session.query(st.Students).all()
    return students
Session.close()