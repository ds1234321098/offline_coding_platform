import sqlalchemy as db
from Engine import Base
class Topic_tag(Base):
    __tablename__ = "topic_tag"
    topic_name = db.Column("topic_name",db.VARCHAR(20),primary_key=True)
    question_id = db.Column("question_id",db.Integer,db.ForeignKey("questions.question_id",ondelete="CASCADE"),primary_key=True)