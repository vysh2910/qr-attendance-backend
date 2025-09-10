from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import AttendanceRecord
from ..schemas import AttendanceMarkIn
from ..core.security import decode_token
import uuid
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/mark")
def mark_attendance(payload: AttendanceMarkIn, db: Session = Depends(get_db)):
    # decode token to get class_id
    try:
        data = decode_token(payload.token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid/expired token")
    if data.get("type") != "attendance_qr":
        raise HTTPException(status_code=400, detail="Bad token")
    class_id = data.get("class_id")
    rec = AttendanceRecord(id=uuid.uuid4(), class_id=class_id, student_id=payload.student_id,
                           method=payload.method, status="present")
    db.add(rec)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Attendance already recorded for this student/class")
    db.refresh(rec)
    return {"ok": True, "attendance_id": str(rec.id)}

