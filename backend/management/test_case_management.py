import os
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database_queries")))
from Engine import session_maker
import questions as qs
import test_cases as tc
test_case_management = APIRouter()
class Test_Case_Entry(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool = True
class Test_Case_Entries(BaseModel):
    test_cases: list[Test_Case_Entry] = Field(min_length=1)
class Test_Case_Update(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool
def test_case_response(data):
    return {
        "test_case_id": data.test_case_id,
        "question_id": data.question_id,
        "input_data": data.input_data,
        "expected_output": data.expected_output,
        "is_hidden": data.is_hidden
    }
@test_case_management.post("/create/{question_id}")
def create_test_cases(question_id: int, entry: Test_Case_Entries):
    Session = session_maker()
    try:
        question = Session.query(qs.Questions).filter(qs.Questions.question_id == question_id).first()
        if question is None:
            raise HTTPException(status_code=404,detail="Question not found")
        new_test_cases = []
        for test_case in entry.test_cases:
            new_test_case = tc.Test_Cases(question_id=question_id,input_data=test_case.input_data,expected_output=test_case.expected_output,is_hidden=test_case.is_hidden)
            new_test_cases.append(new_test_case)
        Session.add_all(new_test_cases)
        Session.commit()
        for test_case in new_test_cases:
            Session.refresh(test_case)
        return {
            "message": "Test cases created successfully",
            "question_id": question_id,
            "test_cases": [
                test_case_response(test_case)
                for test_case in new_test_cases
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        Session.rollback()
        raise HTTPException(status_code=500,detail="An error occurred while creating test cases") from e
    finally:
        Session.close()
@test_case_management.get("/question/{question_id}")
def get_question_test_cases(question_id: int):
    Session = session_maker()
    try:
        question = Session.query(qs.Questions).filter(qs.Questions.question_id == question_id).first()
        if question is None:
            raise HTTPException(status_code=404,detail="Question not found")
        test_cases = Session.query(tc.Test_Cases).filter(tc.Test_Cases.question_id == question_id).order_by(tc.Test_Cases.test_case_id).all()
        return {
            "question_id": question_id,
            "total_test_cases": len(test_cases),
            "test_cases": [
                test_case_response(test_case)
                for test_case in test_cases
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail="An error occurred while retrieving test cases") from e
    finally:
        Session.close()
@test_case_management.get("/{test_case_id}")
def get_test_case(test_case_id: int):
    Session = session_maker()
    try:
        test_case = Session.query(tc.Test_Cases).filter(tc.Test_Cases.test_case_id == test_case_id).first()
        if test_case is None:
            raise HTTPException(status_code=404,detail="Test case not found")
        return test_case_response(test_case)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail="An error occurred while retrieving the test case") from e
    finally:
        Session.close()
@test_case_management.put("/{test_case_id}")
def update_test_case(test_case_id: int, entry: Test_Case_Update):
    Session = session_maker()
    try:
        test_case = Session.query(tc.Test_Cases).filter(tc.Test_Cases.test_case_id == test_case_id).first()
        if test_case is None:
            raise HTTPException(status_code=404,detail="Test case not found")
        test_case.input_data = entry.input_data
        test_case.expected_output = entry.expected_output
        test_case.is_hidden = entry.is_hidden
        Session.commit()
        Session.refresh(test_case)
        return {
            "message": "Test case updated successfully",
            "test_case": test_case_response(test_case)
        }
    except HTTPException:
        raise
    except Exception as e:
        Session.rollback()
        raise HTTPException(status_code=500,detail="An error occurred while updating the test case") from e
    finally:
        Session.close()
@test_case_management.delete("/{test_case_id}")
def delete_test_case(test_case_id: int):
    Session = session_maker()
    try:
        test_case = Session.query(tc.Test_Cases).filter(tc.Test_Cases.test_case_id == test_case_id).first()
        if test_case is None:
            raise HTTPException(status_code=404,detail="Test case not found")
        Session.delete(test_case)
        Session.commit()
        return {
            "message": "Test case deleted successfully",
            "test_case_id": test_case_id
        }
    except HTTPException:
        raise
    except Exception as e:
        Session.rollback()
        raise HTTPException(status_code=500,detail="An error occurred while deleting the test case") from e
    finally:
        Session.close()