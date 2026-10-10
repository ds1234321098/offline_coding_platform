from Engine import Base,engine
from questions import Questions
from sessions import Sessions
from students import Students
from teachers import Teachers
from topic_tag import Topic_tag
from student_enteries_in_session import Student_Enteries
if __name__ == "__main__":
    Base.metadata.create_all(engine)