import sqlalchemy as db
from Engine import Base
class Topic_tag(Base):
    __tablename__ = "topic_tag"
    topic_name = db.Column("topic_name", db.VARCHAR(50), primary_key=True)