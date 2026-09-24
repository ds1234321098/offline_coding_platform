from pydantic import BaseModel
class student(BaseModel):
    name: str
    roll_number: str
    semester: int
    branch: str
students = []
def add(candidate: student):
    for a in students:
        if a.roll_number == candidate.roll_number:
            return False
    students.append(candidate)
    return True
def read(roll_number: str):
    for a in students:
        if a.roll_number == roll_number:
            return a
    return None
def update(roll_number: str, candidate: student):
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