# 🎓 CAMPUSCARE22 - College Grievance & Issue Management System

**CAMPUSCARE22** is a modern, full-stack college complaint and issue tracking web application built with a Python FastAPI backend, SQLite/MySQL database, and a glassmorphism web interface.

---

## 📁 Project Structure

```
CAMPUSCARE22/
├── frontend/
│   ├── index.html               # Main Landing Page with hero section & ticket lookup
│   ├── student-login.html       # Student Sign In & Registration portal
│   ├── staff-login.html         # Staff & Admin Login portal
│   ├── student-dashboard.html   # Student personal complaint dashboard
│   ├── staff-dashboard.html     # Staff control center to filter, update & assign tickets
│   ├── complaint.html           # File a new complaint form
│   ├── status.html              # Track complaint lifecycle timeline
│   ├── css/
│   │   └── style.css            # Modern glassmorphism CSS design system
│   └── js/
│       └── script.js            # Client API logic, session handler & modal controls
│
├── backend/
│   ├── server.py                # Main FastAPI server with CORS & router mount
│   ├── db.py                    # Database connection, table creation & seed data
│   └── routes/
│       ├── student.py           # Student auth endpoints (register/login)
│       ├── staff.py             # Staff auth & employee management endpoints
│       └── complaint.py         # Complaint CRUD, filter, status & timeline updates
│
├── database/
│   └── campus_care22.sql        # MySQL database DDL schema and seed data
│
├── generate_ppt.py              # Python script to generate PowerPoint presentation (.pptx)
├── requirements.txt             # Python dependencies
└── README.md                    # Project Documentation
```

---

## 🚀 How to Run CAMPUSCARE22

### 1. Install Dependencies
Open terminal in `CAMPUSCARE22`:
```bash
pip install -r requirements.txt
```

### 2. Generate PowerPoint Presentation (.pptx)
Run the presentation generator script:
```bash
python generate_ppt.py
```
This produces `CampusCare22_Presentation.pptx`.

### 3. Start Python Backend & Web Server
Run the FastAPI server:
```bash
python -m uvicorn backend.server:app --reload --port 8000
```
- **API URL**: `http://127.0.0.1:8000`
- **Swagger Docs**: `http://127.0.0.1:8000/docs`

---

## 🔑 Demo Login Credentials

### Student Credentials:
- **Roll Number**: `21CS045`
- **Password**: `student123`

### Staff Credentials:
- **Maintenance HOD**: Staff ID `STF101` | Password `staff123`
- **IT Specialist**: Staff ID `STF102` | Password `staff123`
- **Campus Admin**: Staff ID `ADM001` | Password `admin123`
