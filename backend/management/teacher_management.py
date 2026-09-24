from pydantic import BaseModel
class teacher(BaseModel):
    name: str
    username: str
    password: str
teachers = []
def add(candidate: teacher):
    for a in teachers:
        if a.username == candidate.username:
            return False
    teachers.append(candidate)
    return True
def read(username: str):
    for a in teachers:
        if a.username == username:
            return a
    return None
def update(username: str, candidate: teacher):
    for i in range(len(teachers)):
        if teachers[i].username == username:
            teachers[i] = candidate
            return True
    return False
def delete(username: str):
    for i in range(len(teachers)):
        if teachers[i].username == username:
            teachers.pop(i)
            return True
    return False
def get_all():
    return teachers