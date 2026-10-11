import sqlalchemy as db
from Engine import Base
class Question_Topics(Base):
    __tablename__ = "question_topics"
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id", ondelete="CASCADE"), primary_key=True)
    topic_name = db.Column(db.VARCHAR(50), db.ForeignKey("topic_tag.topic_name"), primary_key=True)