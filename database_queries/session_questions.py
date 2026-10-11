import sqlalchemy as db
from Engine import Base
class Session_Questions(Base):
    __tablename__ = "session_questions"
    id = db.Column(db.VARCHAR(10),db.ForeignKey("sessions.id", ondelete="CASCADE"),primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey("questions.question_id", ondelete="CASCADE"),primary_key=True)
    question_number = db.Column(db.Integer,nullable=False)
    __table_args__ = (db.UniqueConstraint("id","question_number",name="unique_session_question_number"),db.CheckConstraint("question_number > 0",name="positive_session_question_number"))