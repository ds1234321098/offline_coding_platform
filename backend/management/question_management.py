import os,sys
from fastapi import APIRouter,HTTPException,FastAPI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..", "database_queries")))
import questions as qs
from Engine import session_maker
from pydantic import BaseModel,Field
questions=FastAPI()
class Question_enteries(BaseModel):
    title:str
    description:str
    input_format:str
    output_format:str
    constraints:str
    time_limit:int=Field(gt=0)
    memory_limit:int=Field(gt=0)
@questions.post("/create")
def create_question(entry:Question_enteries):
    Session=session_maker()
    try:
        data=qs.Questions(title=entry.title,description=entry.description,input_format=entry.input_format,output_format=entry.output_format,constraints=entry.constraints,time_limit=entry.time_limit,memory_limit=entry.memory_limit)
        Session.add(data)
        Session.commit()
        Session.refresh(data)
        return {
            "message":"question created successfully",
            "question_id":data.question_id
        }
    except Exception as a:
        Session.rollback()
        raise HTTPException(status_code=500,detail="error creating question")
    finally:
        Session.close()
@questions.get("/all")
def get_all_questions():
    Session=session_maker()
    try:
        data=Session.query(qs.Questions).order_by(qs.Questions.question_id).all()
        return [
            {
                "question_id":q.question_id,
                "title":q.title,
                "description":q.description,
                "input_format":q.input_format,
                "output_format":q.output_format,
                "constraints":q.constraints,
                "time_limit":q.time_limit,
                "memory_limit":q.memory_limit
            }
            for q in data
        ]
    except Exception as a:
        raise HTTPException(status_code=500,detail="error retrieving questions")
    finally:
        Session.close()
@questions.get("/{question_id}")
def get_question(question_id:int):
    Session=session_maker()
    try:
        data=Session.query(qs.Questions).filter(qs.Questions.question_id==question_id).first()
        if data is None:
            raise HTTPException(status_code=404,detail="question not found")
        return {
            "question_id":data.question_id,
            "title":data.title,
            "description":data.description,
            "input_format":data.input_format,
            "output_format":data.output_format,
            "constraints":data.constraints,
            "time_limit":data.time_limit,
            "memory_limit":data.memory_limit
        }
    except HTTPException:
        raise
    except Exception as a:
        raise HTTPException(status_code=500,detail="error retrieving question")
    finally:
        Session.close()
@questions.put("/{question_id}")
def update_question(question_id:int,entry:Question_enteries):
    Session=session_maker()
    try:
        data=Session.query(qs.Questions).filter(qs.Questions.question_id==question_id).first()
        if data is None:
            raise HTTPException(status_code=404,detail="question not found")
        data.title=entry.title
        data.description=entry.description
        data.input_format=entry.input_format
        data.output_format=entry.output_format
        data.constraints=entry.constraints
        data.time_limit=entry.time_limit
        data.memory_limit=entry.memory_limit
        Session.commit()
        return {
            "message":"question updated successfully",
            "question_id":question_id
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        raise HTTPException(status_code=500,detail="error updating question")
    finally:
        Session.close()
@questions.delete("/{question_id}")
def delete_question(question_id:int):
    Session=session_maker()
    try:
        data=Session.query(qs.Questions).filter(qs.Questions.question_id==question_id).first()
        if data is None:
            raise HTTPException(status_code=404,detail="question not found")
        Session.delete(data)
        Session.commit()
        return {
            "message":"question deleted successfully",
            "question_id":question_id
        }
    except HTTPException:
        raise
    except Exception as a:
        Session.rollback()
        raise HTTPException(status_code=500,detail="error deleting question")
    finally:
        Session.close()