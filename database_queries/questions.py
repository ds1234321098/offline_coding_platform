import sqlalchemy as db
from Engine import Base
class Questions(Base):
    __tablename__="questions"
    question_id=db.Column("question_id",db.Integer,primary_key=True)
    question=db.Column("question",db.Text,nullable=False)