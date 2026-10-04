import sqlalchemy as db
engine=db.create_engine("postresql+psycopg2://dhruvsharma@:localhost:5432/offline_coding_platform")
metadata=db.MetaData()
teachers=db.Table(
    "teachers",metadata,
    db.Column("username",primary_key=True),
    db.Column("name",db.VARCHAR(50),nullable=False),
    db.Column("password_hash",db.VARCHAR(255),nullable=False)
)
metadata.create_all(engine)