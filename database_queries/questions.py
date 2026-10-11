import sqlalchemy as db
from sqlalchemy import Identity
from Engine import Base
class Questions(Base):
    __tablename__ = "questions"
    question_id = db.Column("question_id",db.Integer,Identity(),primary_key=True)
    title = db.Column("title", db.VARCHAR(150), nullable=False)
    description = db.Column("description", db.Text, nullable=False)
    input_format = db.Column("input_format", db.Text, nullable=False)
    output_format = db.Column("output_format", db.Text, nullable=False)
    constraints = db.Column("constraints", db.Text, nullable=False)
    time_limit = db.Column("time_limit",db.Integer,nullable=False)
    memory_limit = db.Column("memory_limit",db.Integer,nullable=False)
    __table_args__ = (db.CheckConstraint("time_limit > 0",name="positive_question_time_limit"),db.CheckConstraint("memory_limit > 0",name="positive_question_memory_limit"))