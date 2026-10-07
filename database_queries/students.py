import sqlalchemy as db
from Engine import Base
class Students(Base):
    __tablename__="students"
    roll_number=db.Column("roll_number",db.VARCHAR(20),primary_key=True)
    name=db.Column("name",db.VARCHAR(50),nullable=False)
    semester=db.Column("semester",db.Integer,nullable=False)
    branch=db.Column("branch",db.VARCHAR(10),nullable=False)
    password_hash=db.Column("password_hash",db.VARCHAR(255),nullable=False)
    __table_args__=(db.CheckConstraint("semester BETWEEN 1 AND 8"),)