---

# QR Attendance Backend

Automated student attendance monitoring system using QR codes.  
Built with **FastAPI**, **PostgreSQL**, and **Docker Compose**.

---

## 🚀 Features
- Faculty can generate QR codes for class sessions.
- Students scan QR to mark attendance.
- Secure JWT tokens ensure integrity & validity (with expiry).
- REST API powered by FastAPI.
- PostgreSQL for persistent storage.

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-org>/qr-attendance-backend.git
cd qr-attendance-backend
````

### 2. Environment configuration

Copy the example `.env` file and adjust values if needed:

```bash
cp .env.example .env
```

Ensure variables like database URL, JWT secret, etc. are set properly.

### 3. Start services with Docker Compose

```bash
docker compose up --build
```

This will spin up:

* `backend` (FastAPI app)
* `db` (Postgres database)

### 4. Seed the database

Run the seed script to populate initial data (users, courses, classes):

```bash
docker compose exec backend python seed_data.py
```

### 5. Verify the API

The backend runs at:
👉 `http://localhost:8000`

API docs (Swagger UI):
👉 `http://localhost:8000/docs`

---

## 🔑 Example Usage

### Generate a QR code for a class

```bash
http POST :8000/api/classes/<class_id>/qr minutes_valid:=5
```

Response includes:

* `qr_image_base64` → QR code image (base64 encoded PNG).
* `token` → JWT token embedded in the QR.

### Mark attendance (student side)

Student scans QR → frontend extracts the token → send to backend:

```bash
http POST :8000/api/attendance/mark token=<jwt_token>
```

If valid, a record is stored in `attendance_records`.

---

## 🗄️ Database Access

Open a Postgres shell:

```bash
docker compose exec db psql -U postgres -d postgres
```

List tables:

```sql
\dt
```

Check attendance records:

```sql
SELECT * FROM attendance_records;
```

---

## 🧑‍💻 Development

### Run backend locally (without Docker)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Make sure Postgres is running and `.env` points to it.

---

## 📌 Notes

* Remove the `version:` field from `docker-compose.yml` (deprecated in recent Docker versions).
* If you hit `ForeignKeyViolation` while seeding, ensure you insert **courses** and **users** before creating **classes**.

---

## 👥 Team

* Backend: FastAPI + SQLAlchemy
* Database: PostgreSQL
* Containerization: Docker Compose

