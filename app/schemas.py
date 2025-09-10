from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ClassCreate(BaseModel):
    course_id: str
    faculty_id: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str]

class QRResponse(BaseModel):
    token: str
    qr_image_base64: str

class AttendanceMarkIn(BaseModel):
    student_id: str
    token: str
    method: Optional[str] = "qr"

