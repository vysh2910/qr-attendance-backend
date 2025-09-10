from fastapi import FastAPI
from .db import engine, Base
from .routes import auth, classes, attendance

app = FastAPI(title="QR Attendance Backend")

# include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(classes.router, prefix="/api/classes", tags=["classes"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["attendance"])

@app.on_event("startup")
def startup():
    # create DB tables (fast for hackathon)
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"ok": True}

