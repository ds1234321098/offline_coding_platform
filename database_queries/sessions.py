import sqlalchemy as db
from Engine import Base
from create_session_id import create_session_id
class Sessions(Base):
    __tablename__ = "sessions"
    id = db.Column(db.VARCHAR(10),primary_key=True, default=create_session_id)
    branch = db.Column(db.VARCHAR(length=10),nullable=False)
    semester = db.Column(db.Integer,nullable=False)
    session_date = db.Column(db.Date,nullable=False)
    session_time = db.Column(db.Time,nullable=False)
    status = db.Column(db.VARCHAR(length=7),nullable=False,default='active')
    __table_args__ = (db.CheckConstraint("semester BETWEEN 1 AND 8"),db.CheckConstraint("status IN ('active', 'ended')"))