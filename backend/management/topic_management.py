import os,sys
from fastapi import APIRouter,HTTPException,FastAPI
from pydantic import BaseModel,Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
from Engine import session_maker
import questions as qs
import topic_tag as tt
import question_topics as qt
topic_management=APIRouter()
class Topic_Enteries(BaseModel):
    topic_name:str=Field(min_length=1,max_length=50)
class Question_Topic_Enteries(BaseModel):
    question_id: int = Field(gt=0)
    topic_name: list[str] = Field(min_length=1)
class Single_Question_Topic_Enteries(BaseModel):
    question_id:int=Field(gt=0)
    topic_name:str=Field(min_length=1,max_length=50)
@topic_management.post("/create_topic")
def create_topic(entry:Topic_Enteries):
    Session=session_maker()
    try:
        topic=entry.topic_name.strip()
        if not topic:
            raise HTTPException(status_code=400,detail="topic name cannot be empty")
        data=Session.query(tt.Topic_tag).filter(tt.Topic_tag.topic_name==topic).first()
        if data is not None:
            raise HTTPException(status_code=400,detail="topic already exists")
        s1=tt.Topic_tag(topic_name=topic)
        Session.add(s1)
        Session.commit()
        return {
            "message":"topic added successfully",
            "topic_name":topic
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        raise HTTPException(status_code=500,detail="error creating topic")
    finally:
        Session.close()
@topic_management.get("/get_all_topics")
def get_all_topics():
    Session=session_maker()
    try:
        data=Session.query(tt.Topic_tag).order_by(tt.Topic_tag.topic_name).all()
        return {
            "topics":[
                {"topic_name":a.topic_name}
                for a in data
            ]
        }
    except Exception as a:
        raise HTTPException(status_code=500,detail="error retrieving topics")
    finally:
        Session.close()
@topic_management.post("/assign_topic")
def assign_topic(entry: Question_Topic_Enteries):
    Session = session_maker()
    try:
        question = Session.query(qs.Questions).filter(qs.Questions.question_id == entry.question_id).first()
        if question is None:
            raise HTTPException(status_code=404,detail="question not found")
        topic_names = list(dict.fromkeys(name.strip() for name in entry.topic_name))
        if any(not name for name in topic_names):
            raise HTTPException(status_code=400,detail="topic names cannot be empty")
        existing_topics = Session.query(tt.Topic_tag).filter(tt.Topic_tag.topic_name.in_(topic_names)).all()
        existing_topic_names = {topic.topic_name for topic in existing_topics}
        missing_topics = [
            name for name in topic_names
            if name not in existing_topic_names
        ]
        if missing_topics:
            raise HTTPException(status_code=404,
                detail={"message": "some topics do not exist","missing_topics": missing_topics})
        existing_assignments = Session.query(qt.Question_Topics).filter(qt.Question_Topics.question_id == entry.question_id,qt.Question_Topics.topic_name.in_(topic_names)).all()
        already_assigned = {
            assignment.topic_name
            for assignment in existing_assignments
        }
        new_assignments = [
            name for name in topic_names
            if name not in already_assigned
        ]
        for name in new_assignments:
            data = qt.Question_Topics(question_id=entry.question_id,topic_name=name)
            Session.add(data)
        Session.commit()
        return {
            "message": "topic assignment completed",
            "question_id": entry.question_id,
            "assigned_topics": new_assignments,
            "already_assigned": list(already_assigned)
        }
    except HTTPException:
        raise
    except Exception:
        Session.rollback()
        raise HTTPException(status_code=500,detail="error assigning topics")
    finally:
        Session.close()
@topic_management.get("/question_topics/{question_id}")
def get_question_topics(question_id:int):
    Session=session_maker()
    try:
        question=Session.query(qs.Questions).filter(qs.Questions.question_id==question_id).first()
        if question is None:
            raise HTTPException(status_code=404,detail="question not found")
        data=Session.query(qt.Question_Topics).filter(qt.Question_Topics.question_id==question_id).order_by(qt.Question_Topics.topic_name).all()
        return {
            "question_id":question_id,
            "topics":[
                a.topic_name
                for a in data
            ]
        }
    except HTTPException:
        raise
    except Exception as a:
        raise HTTPException(status_code=500,detail="error retrieving question topics")
    finally:
        Session.close()
@topic_management.get("/topic_questions/{topic_name}")
def get_topic_questions(topic_name:str):
    Session=session_maker()
    try:
        topic=Session.query(tt.Topic_tag).filter(tt.Topic_tag.topic_name==topic_name).first()
        if topic is None:
            raise HTTPException(status_code=404,detail="topic not found")
        data=Session.query(qs.Questions).join(
            qt.Question_Topics,qs.Questions.question_id==qt.Question_Topics.question_id).filter(qt.Question_Topics.topic_name==topic_name).order_by(qs.Questions.question_id).all()
        return {
            "topic_name":topic_name,
            "questions":[
                {
                    "question_id":a.question_id,
                    "title":a.title
                }
                for a in data
            ]
        }
    except HTTPException:
        raise
    except Exception as a:
        raise HTTPException(status_code=500,detail="error retrieving topic questions")
    finally:
        Session.close()
@topic_management.delete("/remove_topic")
def remove_topic(entry:Single_Question_Topic_Enteries):
    Session=session_maker()
    try:
        data=Session.query(qt.Question_Topics).filter(qt.Question_Topics.question_id==entry.question_id,qt.Question_Topics.topic_name==entry.topic_name).first()
        if data is None:
            raise HTTPException(status_code=404,detail="topic assignment not found")
        Session.delete(data)
        Session.commit()
        return {
            "message":"topic removed from question successfully",
            "question_id":entry.question_id,
            "topic_name":entry.topic_name
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        raise HTTPException(status_code=500,detail="error removing topic")
    finally:
        Session.close()
@topic_management.delete("/delete_topic/{topic_name}")
def delete_topic(topic_name:str):
    Session=session_maker()
    try:
        data=Session.query(tt.Topic_tag).filter(tt.Topic_tag.topic_name==topic_name).first()
        if data is None:
            raise HTTPException(status_code=404,detail="topic not found")
        Session.delete(data)
        Session.commit()
        return {
            "message":"topic deleted successfully",
            "topic_name":topic_name
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        raise HTTPException(status_code=500,detail="error deleting topic")
    finally:
        Session.close()