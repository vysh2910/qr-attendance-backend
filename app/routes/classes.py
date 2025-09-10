from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import ClassSession
from ..schemas import ClassCreate, QRResponse
from ..core.security import create_access_token
import qrcode, io, base64, uuid

router = APIRouter()

@router.post("/", response_model=dict)
def create_class(payload: ClassCreate, db: Session = Depends(get_db)):
    cs = ClassSession(id=uuid.uuid4(), course_id=payload.course_id, faculty_id=payload.faculty_id,
                      start_time=payload.start_time, end_time=payload.end_time, location=payload.location)
    db.add(cs)
    db.commit()
    db.refresh(cs)
    return {"id": str(cs.id)}

@router.post("/{class_id}/qr", response_model=QRResponse)
def generate_qr(class_id: str, minutes_valid: int = 5):
    # Create a short-lived JWT token for marking attendance
    payload = {"class_id": class_id, "type": "attendance_qr"}
    token = create_access_token(payload, expires_minutes=minutes_valid)
    # Create QR (we embed the token; in production you may embed a URL)
    # For demo we'll encode the token as data so the student app posts the token to /attendance/mark
    img = qrcode.make(token)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return {"token": token, "qr_image_base64": f"data:image/png;base64,{b64}"}

