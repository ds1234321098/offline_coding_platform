import sqlalchemy as db
from Engine import Base
class Session_Topics(Base):
    __tablename__ = "session_topics"
    id = db.Column(db.VARCHAR(10),db.ForeignKey("sessions.id", ondelete="CASCADE"),primary_key=True)
    topic_tag = db.Column(db.VARCHAR(50),db.ForeignKey("topic_tag.topic_name",ondelete="CASCADE"),primary_key=True)