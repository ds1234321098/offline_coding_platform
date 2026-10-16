import random
import os
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","database_queries")))
from Engine import session_maker
import topic_tag as tt
import questions as qs
import question_topics as qt
import session_questions as sq
import session_topics as st
import sessions as ss
s_q_management = APIRouter()
class S_Q_Management(BaseModel):
    session_id: str = Field(min_length=1, max_length=10)
    topics: list[str] = Field(min_length=1)
    number_of_questions: int = Field(gt=0)
@s_q_management.post("/assign_topics")
def assign(data: S_Q_Management):
    Session = session_maker()
    try:
        topic_names = list(dict.fromkeys(topic.strip() for topic in data.topics))
        if any(not topic for topic in topic_names):
            raise HTTPException(status_code=400,detail="Topic names cannot be empty")
        session = Session.query(ss.Sessions).filter(ss.Sessions.id == data.session_id).first()
        if session is None:
            raise HTTPException(status_code=404,detail="Session not found")
        if session.status=='ended':
            raise HTTPException(status_code=404,detail="session already ended")
        existing_topics = Session.query(tt.Topic_tag).filter(tt.Topic_tag.topic_name.in_(topic_names)).all()
        existing_topic_names = {topic.topic_name for topic in existing_topics}
        missing_topics = [
            topic
            for topic in topic_names
            if topic not in existing_topic_names
        ]
        if missing_topics:
            raise HTTPException(status_code=404,detail={"message": "Some topics were not found","missing_topics": missing_topics})
        existing_questions = Session.query(sq.Session_Questions).filter(sq.Session_Questions.id == data.session_id).first()
        if existing_questions is not None:
            raise HTTPException(status_code=409,detail="Questions have already been assigned to this session")
        existing_session_topics = Session.query(st.Session_Topics).filter(st.Session_Topics.id == data.session_id).all()
        existing_session_topic_names = {
            topic.topic_tag
            for topic in existing_session_topics
        }
        if (existing_session_topic_names and existing_session_topic_names != set(topic_names)):
            raise HTTPException(status_code=409,detail={"message": "Different topics have already been assigned to this session","existing_topics": sorted(existing_session_topic_names)})
        question_rows = Session.query(qt.Question_Topics.question_id).filter(qt.Question_Topics.topic_name.in_(topic_names)).distinct().all()
        question_ids = [
            row[0]
            for row in question_rows
        ]
        if len(question_ids) < data.number_of_questions:
            raise HTTPException(status_code=400,detail={"message": "Not enough questions are available for the selected topics","available_questions": len(question_ids),"requested_questions": data.number_of_questions})
        selected_question_ids = random.sample(question_ids,data.number_of_questions)
        if not existing_session_topic_names:
            for topic_name in topic_names:
                topic_entry = st.Session_Topics(id=data.session_id,topic_tag=topic_name)
                Session.add(topic_entry)
        for question_number, question_id in enumerate(selected_question_ids,start=1):
            question_entry = sq.Session_Questions(id=data.session_id,question_id=question_id,question_number=question_number)
            Session.add(question_entry)
        Session.commit()
        return {
            "message": "Topics and questions assigned successfully",
            "session_id": data.session_id,
            "selected_topics": topic_names,
            "number_of_questions": len(selected_question_ids),
            "assigned_questions": [
                {
                    "question_number": question_number,
                    "question_id": question_id
                }
                for question_number, question_id in enumerate(
                    selected_question_ids,
                    start=1
                )
            ]
        }
    except HTTPException:
        Session.rollback()
        raise
    except Exception:
        Session.rollback()
        raise HTTPException(status_code=500,detail="Error assigning topics and questions to session")
    finally:
        Session.close()