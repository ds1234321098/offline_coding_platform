import sqlalchemy as db
from sqlalchemy.sql import func
from Engine import Base
class Submissions(Base):
    __tablename__ = "submissions"
    submission_id = db.Column("submission_id",db.Integer,db.Identity(),primary_key=True)
    session_id = db.Column("session_id",db.VARCHAR(10),db.ForeignKey("sessions.id", ondelete="CASCADE"),nullable=False)
    roll_number = db.Column("roll_number",db.VARCHAR(50),db.ForeignKey("students.roll_number", ondelete="CASCADE"),nullable=False)
    question_id = db.Column("question_id",db.Integer,db.ForeignKey("questions.question_id", ondelete="CASCADE"),nullable=False)
    language = db.Column("language",db.VARCHAR(20),nullable=False)
    source_code = db.Column("source_code",db.Text,nullable=False)
    status = db.Column("status",db.VARCHAR(30),nullable=False,default="QUEUED",server_default="QUEUED")
    submitted_at = db.Column("submitted_at",db.DateTime(timezone=True),nullable=False,server_default=func.now())