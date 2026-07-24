# CampusScan 🛡️
### College Complaint Management System

CampusScan is a full-stack web application that lets **students** report campus issues
(infrastructure, hostel, academic, harassment, ragging, canteen, etc.) and lets **staff**
track, prioritize, and resolve them — all through separate, role-based login portals.

---

## ✨ Features

- Separate **Student Login/Register** and **Staff Login** portals (JWT-secured)
- Students can file complaints with category, priority, location, and optional anonymity
- Real-time complaint status tracking: `Pending → In Progress → Resolved / Rejected`
- Staff dashboard with live stats, filters (status/category), and inline status updates
- Staff can respond directly to each complaint; response is visible to the student
- Passwords hashed with **bcrypt**; sessions secured with **JWT**
- Clean, responsive UI — no framework dependency on the frontend (pure HTML/CSS/JS)

---

## 🗂️ Project Structure

```
CampusScan/
│
├── frontend/                  # Static client (HTML/CSS/JS)
│   ├── index.html             # Landing page
│   ├── student-login.html     # Student login + registration
│   ├── staff-login.html       # Staff login
│   ├── student-dashboard.html # Student overview & recent complaints
│   ├── staff-dashboard.html   # Staff overview, filters & complaint management
│   ├── complaint.html         # File a new complaint
│   ├── status.html            # Track my complaints
│   ├── css/style.css
│   └── js/script.js
│
├── backend/                   # Node.js + Express API
│   ├── server.js
│   ├── db.js
│   ├── middleware/auth.js     # JWT verification
│   └── routes/
│       ├── student.js         # /api/student/*
│       ├── staff.js           # /api/staff/*
│       └── complaint.js       # /api/complaint/*
│
├── database/
│   └── campus_scan.sql        # MySQL schema + seed data
│
├── package.json
└── .env.example
```

---

## ⚙️ Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Frontend   | HTML5, CSS3, Vanilla JavaScript      |
| Backend    | Node.js, Express.js                  |
| Database   | MySQL                                |
| Auth       | JWT (jsonwebtoken) + bcrypt          |

---

## 🚀 Setup Instructions

### 1. Install dependencies
```bash
npm install
```

### 2. Set up the database
- Create the schema by running the SQL file in MySQL:
```bash
mysql -u root -p < database/campus_scan.sql
```
This creates the `campus_scan` database, its tables, and two demo accounts:

| Role    | Email                      | Password     |
|---------|-----------------------------|--------------|
| Student | arun.student@campus.edu     | password123  |
| Staff   | ramesh.staff@campus.edu     | password123  |

### 3. Configure environment variables
Copy `.env.example` to `.env` and fill in your MySQL credentials:
```bash
cp .env.example .env
```

### 4. Run the server
```bash
npm start
```
The app will be available at **http://localhost:5000**

---

## 🔌 API Overview

| Method | Endpoint                     | Access   | Description                     |
|--------|-------------------------------|----------|----------------------------------|
| POST   | /api/student/register         | Public   | Register a new student           |
| POST   | /api/student/login            | Public   | Student login                    |
| GET    | /api/student/profile          | Student  | Get logged-in student profile    |
| POST   | /api/staff/login              | Public   | Staff login                      |
| GET    | /api/staff/stats              | Staff    | Dashboard summary counts         |
| POST   | /api/complaint/add            | Student  | File a new complaint             |
| GET    | /api/complaint/my             | Student  | List my complaints               |
| GET    | /api/complaint/all            | Staff    | List all complaints (filterable) |
| PUT    | /api/complaint/update/:id     | Staff    | Update status / add response     |
| GET    | /api/complaint/:id             | Both     | Get a single complaint           |

---

## 🎓 Academic Note

This project was built as a college mini-project demonstrating a role-based grievance/
complaint management system, covering authentication, CRUD operations, and a
student–staff workflow end to end.
