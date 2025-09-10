import os
import uuid
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import Student, Course, ClassSession

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

course = Course(id=uuid.uuid4(), code="CS101", title="Sample Course")
db.add(course)
student = Student(id=uuid.uuid4(), roll_no="2025CS001", name="Test Student", email="student@example.com")
db.add(student)
cs = ClassSession(id=uuid.uuid4(), course_id=course.id)
db.add(cs)
db.commit()
print("seeded:", str(course.id), str(student.id), str(cs.id))
db.close()

