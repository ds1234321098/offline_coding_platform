import sqlalchemy as db
from sqlalchemy.orm import declarative_base,sessionmaker
engine=db.create_engine("postgresql+psycopg2://dhruvsharma:@localhost:5432/offline_coding_platform")
Base=declarative_base()
session_maker=sessionmaker(bind=engine)