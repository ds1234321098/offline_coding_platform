import os
import sys
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","database_queries")))
from Engine import session_maker
import students as st
import sessions as ss
import student_enteries_in_session as seis
import session_questions as sq
import submissions as sub
student_submission = APIRouter()
class Student_Submission(BaseModel):
    session_id: str = Field(min_length=1, max_length=10)
    roll_number: str = Field(min_length=1, max_length=50)
    question_id: int = Field(gt=0)
    language: str = Field(min_length=1, max_length=20)
    source_code: str = Field(min_length=1, max_length=100000000000)
@student_submission.post("/submit")
def submit_code(entry: Student_Submission):
    Session = session_maker()
    try:
        session = Session.query(ss.Sessions).filter(ss.Sessions.id == entry.session_id).first()
        if session is None:
            raise HTTPException(status_code=404,detail="Session not found")
        if session.status != "active":
            raise HTTPException(status_code=403,detail="This session is not active")
        student = Session.query(st.Students).filter(st.Students.roll_number == entry.roll_number).first()
        if student is None:
            raise HTTPException(status_code=404,detail="Student not found")
        participation = Session.query(seis.Student_Enteries).filter(seis.Student_Enteries.id == entry.session_id,seis.Student_Enteries.roll_number == entry.roll_number).first()
        if participation is None:
            raise HTTPException(status_code=403,detail="Student has not joined this session")
        if participation.status != "Present":
            raise HTTPException(status_code=403,detail="Student is not currently participating in this session")
        assigned_question = Session.query(sq.Session_Questions).filter(sq.Session_Questions.id == entry.session_id,sq.Session_Questions.question_id == entry.question_id).first()
        if assigned_question is None:
            raise HTTPException(status_code=403,detail="This question is not assigned to the session")
        allowed_languages = {"cpp","python","java"}
        language = entry.language.strip().lower()
        if language not in allowed_languages:
            raise HTTPException(status_code=422,detail="Unsupported language. Use cpp, python, or java")
        new_submission = sub.Submissions(session_id=entry.session_id,roll_number=entry.roll_number,question_id=entry.question_id,language=language,source_code=entry.source_code,status="QUEUED")
        Session.add(new_submission)
        Session.commit()
        Session.refresh(new_submission)
        return {
            "message": "Code submitted successfully",
            "submission_id": new_submission.submission_id,
            "session_id": new_submission.session_id,
            "roll_number": new_submission.roll_number,
            "question_id": new_submission.question_id,
            "language": new_submission.language,
            "status": new_submission.status,
            "submitted_at": new_submission.submitted_at
        }
    except HTTPException:
        raise
    except Exception as e:
        Session.rollback()
        raise HTTPException(status_code=500,detail="An error occurred while submitting the code") from e
    finally:
        Session.close()