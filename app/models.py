import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from .db import Base

# Use PG_UUID if Postgres, else String for sqlite compatibility
UUID_TYPE = PG_UUID(as_uuid=True)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    role = Column(String, nullable=False, default="faculty")
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Student(Base):
    __tablename__ = "students"
    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    roll_no = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Course(Base):
    __tablename__ = "courses"
    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    title = Column(String, nullable=False)

class ClassSession(Base):
    __tablename__ = "classes"
    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID_TYPE, ForeignKey("courses.id"))
    faculty_id = Column(UUID_TYPE, ForeignKey("users.id"))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    class_id = Column(UUID_TYPE, ForeignKey("classes.id"), nullable=False)
    student_id = Column(UUID_TYPE, ForeignKey("students.id"), nullable=False)
    status = Column(String, nullable=False, default="present")
    method = Column(String, nullable=False, default="qr")
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    extra_data = Column(JSON)
    __table_args__ = (UniqueConstraint("class_id", "student_id", name="uix_class_student"),)

