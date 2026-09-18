<div align="center">

  <h1>🎓 CAMPUSCARE22</h1>
  <p><strong>College Grievance & Maintenance Issue Tracking System</strong></p>

  <!-- GitHub Badges (Shields.io) -->
  <p>
    <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" /></a>
    <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /></a>
    <a href="https://sqlite.org"><img src="https://img.shields.io/badge/SQLite-Embedded%20DB-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" /></a>
    <a href="https://github.com/Praventh5561/Campus-Care"><img src="https://img.shields.io/badge/YOLO-Badge%20🤠-ff69b4?style=for-the-badge&logo=github" alt="YOLO Mode" /></a>
    <a href="https://github.com/Praventh5561/Campus-Care/pulls"><img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge" alt="PRs Welcome" /></a>
    <a href="https://github.com/Praventh5561/Campus-Care/stargazers"><img src="https://img.shields.io/badge/⭐%20Stars-Appreciate-yellow?style=for-the-badge" alt="Stars" /></a>
  </p>

</div>

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
```bash
pip install -r requirements.txt
```

### 2. Generate PowerPoint Presentation (.pptx)
```bash
python generate_ppt.py
```
This produces `CampusCare22_Presentation.pptx`.

### 3. Start Python Backend & Web Server
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
