import sqlalchemy as db
from Engine import Base
class Teachers(Base):
    __tablename__="teachers"
    username=db.Column("username",db.VARCHAR(50),primary_key=True)
    name=db.Column("name",db.VARCHAR(50),nullable=False)
    password_hash=db.Column("password_hash",db.VARCHAR(255),nullable=False)