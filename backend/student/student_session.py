from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
student_session = APIRouter()
class join_session_class(BaseModel):
    roll_number: str
    session_id: str
joined_students = []
@student_session.post("/join")
def join_session(candidate: join_session_class):
    for student in joined_students:
        if (student["roll_number"] == candidate.roll_number and student["session_id"] == candidate.session_id):
            raise HTTPException(status_code=400,detail="Student has already joined this session")
    joined_students.append({
        "roll_number": candidate.roll_number,
        "session_id": candidate.session_id
    })
    return {
        "message": "Session joined successfully",
        "roll_number": candidate.roll_number,
        "session_id": candidate.session_id
    }
@student_session.get("/students/{session_id}")
def get_students(session_id: str):
    students = []
    for student in joined_students:
        if student["session_id"] == session_id:
            students.append(student["roll_number"])
    return {
        "session_id": session_id,
        "students": students
    }