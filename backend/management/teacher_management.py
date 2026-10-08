from pydantic import BaseModel
import sys
import os
from password_hash import hash_password
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
import Engine
import teachers as tc
session=sessionmaker(bind=Engine.engine)
Session=session()
class teacher_class(BaseModel):
    name: str
    username: str
    password: str
def add(candidate: teacher_class):
    teachers=Session.query(tc.Teachers).all()
    for a in teachers:
        if a.username == candidate.username:
            return False
    new_teacher=tc.Teachers(username=candidate.username,name=candidate.name,password_hash=hash_password(candidate.password))
    Session.add(new_teacher)
    Session.commit()
    return True
def read(username: str):
    teachers=Session.query(tc.Teachers).all()
    for a in teachers:
        if a.username == username:
            return a
    return None
def update(username: str, candidate: teacher_class):
    try:
        teachers=Session.query(tc.Teachers).all()
        with Session.begin_nested():
            for teacher in teachers:
                if teacher.username==username:
                    (Session.query(tc.Teachers).filter_by(username=username).all())[0].name=candidate.name
                    (Session.query(tc.Teachers).filter_by(username=username).all())[0].password_hash=hash_password(candidate.password)
                    Session.commit()
                    return True
            return False
    except Exception as a:
        print(f"error is : {a}")
def delete(username: str):
    teachers=Session.query(tc.Teachers).all()
    for teacher in teachers:
        if teacher.username==username:
            Session.delete(teacher)
            Session.commit()
            return True
    return False
def get_all():
    teachers=Session.query(tc.Teachers).all()
    return teachers
Session.close()