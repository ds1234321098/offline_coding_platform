import sqlalchemy as db
engine=db.create_engine("postresql+psycopg2://dhruvsharma@:localhost:5432/offline_coding_platform")
metadata_obj=db.MetaData()
students=db.Table(
    "students",metadata_obj,
    db.Column("roll_number",db.VARCHAR(20),primary_key=True),
    db.Column("name",db.VARCHAR(20),nullable=False),
    db.Column("semester",db.Integer,nullable=False),
    db.CheckConstraint("semester BETWEEN 1 AND 8"),
    db.Column("branch",db.VARCHAR(5),nullable=False),
    db.Column("password_hash",db.VARCHAR(255),nullable=False)
)
metadata_obj.create_all(engine)