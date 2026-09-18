from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from backend.db import get_db

router = APIRouter(prefix="/api/student", tags=["Student Authentication"])

class StudentRegister(BaseModel):
    roll_number: str
    name: str
    email: str
    password: str
    department: str
    year_of_study: int = 1
    phone: Optional[str] = ""

class StudentLogin(BaseModel):
    roll_number: str
    password: str

@router.post("/register")
def register_student(student: StudentRegister):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM students WHERE roll_number = ? OR email = ?", (student.roll_number, student.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this Roll Number or Email already exists."
        )

    cursor.execute("""
        INSERT INTO students (roll_number, name, email, password, department, year_of_study, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student.roll_number, student.name, student.email, student.password, student.department, student.year_of_study, student.phone))
    
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    return {
        "success": True,
        "message": "Student registered successfully!",
        "user": {
            "id": student_id,
            "roll_number": student.roll_number,
            "name": student.name,
            "email": student.email,
            "department": student.department,
            "role": "student"
        }
    }

@router.post("/login")
def login_student(credentials: StudentLogin):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, roll_number, name, email, department, year_of_study, phone, password 
        FROM students WHERE roll_number = ?
    """, (credentials.roll_number,))
    
    row = cursor.fetchone()
    conn.close()

    if not row or row["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Roll Number or Password."
        )

    return {
        "success": True,
        "message": "Login successful!",
        "user": {
            "id": row["id"],
            "roll_number": row["roll_number"],
            "name": row["name"],
            "email": row["email"],
            "department": row["department"],
            "year_of_study": row["year_of_study"],
            "role": "student"
        }
    }
