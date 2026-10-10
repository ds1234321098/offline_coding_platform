from Engine import Base
import sqlalchemy as db
class Student_Enteries(Base):
    __tablename__="student_enteries"
    id=db.Column("id",db.VARCHAR(10),db.ForeignKey("sessions.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    roll_number=db.Column("roll_number",db.VARCHAR(20),db.ForeignKey("students.roll_number",ondelete="CASCADE"),nullable=False,primary_key=True)
    status=db.Column("status",db.VARCHAR(10),db.CheckConstraint("status in ('Present','Left')"),nullable=False,default='Present')