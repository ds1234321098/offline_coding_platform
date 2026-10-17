import sqlalchemy as db
from Engine import Base, engine
from questions import Questions
from sessions import Sessions
from students import Students
from teachers import Teachers
from topic_tag import Topic_tag
from student_enteries_in_session import Student_Enteries
from session_questions import Session_Questions
from question_topics import Question_Topics
from session_topics import Session_Topics
from test_cases import Test_Cases
from submissions import Submissions
def initialize():
    Base.metadata.create_all(engine)
    with engine.begin() as connection:
        connection.execute(db.text("""
            CREATE SEQUENCE IF NOT EXISTS session_id_sequence
                START WITH 1
                INCREMENT BY 1
                MINVALUE 1
                MAXVALUE 2000000000
                NO CYCLE;
        """))
if __name__ == "__main__":
    initialize()
def reset_counter():
    with engine.begin() as conn:
        conn.execute(db.text("TRUNCATE TABLE sessions CASCADE;"))
        conn.execute(db.text("ALTER SEQUENCE session_id_sequence RESTART WITH 1;"))
def reset_questions_sequence():
    with engine.begin() as conn:
        conn.execute(db.text("TRUNCATE TABLE questions RESTART IDENTITY CASCADE;"))