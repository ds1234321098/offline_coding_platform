import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database_queries")))
import create_db
from fastapi import FastAPI
from teacher.teacher_session import session
from auth.teacher_auth import auth as auth1
from auth.student_auth import auth as auth2
from student.student_session import student_session
from management.question_management import questions
from management.topic_management import topic_management
from teacher.session_question_management import s_q_management
app = FastAPI(
    title="Offline Coding Platform",
    description="Backend API for the university coding platform",
    version="1.0.0"
)
app.include_router(
    session,
    prefix="/teacher/session",
    tags=["Teacher Session Management"]
)
app.include_router(
    student_session,
    prefix="/student/session",
    tags=["Student Session Management"]
)
app.include_router(
    questions,
    prefix="/questions",
    tags=["Question Management"]
)
app.include_router(
    topic_management,
    prefix="/topics",
    tags=["Topic Management"]
)
app.include_router(
    s_q_management,
    prefix="/teacher/session/questions",
    tags=["Session Question Assignment"]
)
app.include_router(
    auth1,
    prefix="/teacher_auth",
    tags=["Teacher Authenticator"]
)
app.include_router(
    auth2,
    prefix="/student_auth",
    tags=["Student Authenticator"]
)
@app.get("/")
def home():
    return {
        "message": "Offline Coding Platform API is running"
    }
@app.get("/health")
def health():
    return {
        "status": "running"
    }