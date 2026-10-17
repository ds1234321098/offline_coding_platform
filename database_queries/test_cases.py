from Engine import Base
import sqlalchemy as db
class Test_Cases(Base):
    __tablename__ = "test_cases"
    test_case_id = db.Column("test_case_id",db.Integer,db.Identity(),primary_key=True)
    question_id = db.Column("question_id",db.Integer,db.ForeignKey("questions.question_id",ondelete="CASCADE"),nullable=False)
    input_data = db.Column("input_data",db.Text,nullable=False)
    expected_output = db.Column("expected_output",db.Text,nullable=False)
    is_hidden = db.Column("is_hidden",db.Boolean,nullable=False,default=True,server_default=db.true())