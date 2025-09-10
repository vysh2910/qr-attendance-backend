import uuid
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import Student, Course, ClassSession

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# 1. Create and commit a course
course = Course(id=uuid.uuid4(), code="CS101", title="Sample Course")
db.add(course)
db.commit()
db.refresh(course)

# 2. Create and commit a student
student = Student(id=uuid.uuid4(), roll_no="2025CS001", name="Test Student", email="student@example.com")
db.add(student)
db.commit()
db.refresh(student)

# 3. Now create and commit a class that links to the committed course
cs = ClassSession(id=uuid.uuid4(), course_id=course.id, faculty_id=None)
db.add(cs)
db.commit()
db.refresh(cs)

print("==> Seeded successfully:")
print("Course ID:", str(course.id))
print("Student ID:", str(student.id))
print("Class ID:", str(cs.id))

db.close()

