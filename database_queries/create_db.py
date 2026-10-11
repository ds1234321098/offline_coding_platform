from Engine import Base,engine
from questions import Questions
from sessions import Sessions
from students import Students
from teachers import Teachers
from topic_tag import Topic_tag
from student_enteries_in_session import Student_Enteries
from session_questions import Session_Questions
from question_topics import Question_Topics
from session_topics import Session_Topics
if __name__ == "__main__":
    Base.metadata.create_all(engine)