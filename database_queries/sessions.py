import sqlalchemy as db
engine=db.create_engine("postresql+psycopg2://dhruvsharma@:localhost:5432/offlie_coding_platform")
metadata_obj=db.MetaData()
sessions=db.Table(
    "sessions",metadata_obj,
    db.Column("id",db.UUID,primary_key=True),
    db.Column("branch",db.VARCHAR(length=10),nullable=False),
    db.Column("semester",db.Integer,nullable=False),
    db.CheckConstraint("semester BETWEEN 1 AND 8"),
    db.Column("session_date",db.Date,nullable=False),
    db.Column("session_time",db.Time,nullable=False),
    db.Column("status",db.VARCHAR(7),nullable=False),
    db.CheckConstraint("status IN ('active,'ended)")
)
metadata_obj.create_all(engine)