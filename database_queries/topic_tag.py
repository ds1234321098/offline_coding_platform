import sqlalchemy as db
engine=db.create_engine("postresql+psycopg2://dhruvsharma@:localhost:5432/offline_coding_platform")
metadata=db.MetaData()
topic_tag=db.Table(
    "topic_tag",metadata,
    db.Column("topic_name",db.VARCHAR(20),unique=True,nullable=False),
    db.Column("question_id",db.Integer,db.ForeignKey("questions.question_id",ondelete="CASCADE"),nullable=False)
)
metadata.create_all(engine)