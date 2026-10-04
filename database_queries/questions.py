import sqlalchemy as db
engine=db.create_engine("postresql+psycopg2://dhruvsharma:@localhost:5432/offline_coding_platform")
metadata_obj=db.MetaData()
questions=db.Table(
    "questions",metadata_obj,
    db.Column("question_id",db.Integer,primary_key=True),
    db.Column("question",db.Text,nullable=False)
)
metadata_obj.create_all(engine)