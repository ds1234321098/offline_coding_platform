from Engine import Base,engine
from questions import Questions
from sessions import Sessions
from students import Students
from teachers import Teachers
from topic_tag import Topic_tag
if __name__ == "__main__":
    Base.metadata.create_all(engine)