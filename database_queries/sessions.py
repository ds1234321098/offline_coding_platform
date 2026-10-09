import uuid
import sqlalchemy as db
from Engine import Base
class Sessions(Base):
    __tablename__ = "sessions"
    id = db.Column(db.VARCHAR(10), primary_key=True, default=uuid.uuid4)
    branch = db.Column(db.VARCHAR(length=10),nullable=False)
    semester = db.Column(db.Integer,nullable=False)
    session_date = db.Column(db.Date,nullable=False)
    session_time = db.Column(db.Time,nullable=False)
    status = db.Column(db.VARCHAR(length=7),nullable=False)
    __table_args__ = (db.CheckConstraint("semester BETWEEN 1 AND 8"),db.CheckConstraint("status IN ('active', 'ended')"))