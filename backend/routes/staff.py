from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from backend.db import get_db
from backend.security import hash_password, verify_password, generate_session_token

router = APIRouter(prefix="/api/staff", tags=["Staff Authentication & Management"])

class StaffLogin(BaseModel):
    staff_id: str
    password: str

@router.post("/login")
def login_staff(credentials: StaffLogin):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, staff_id, name, email, department, role, password 
        FROM staff WHERE staff_id = ?
    """, (credentials.staff_id,))
    
    row = cursor.fetchone()
    conn.close()

    if not row or not verify_password(credentials.password, row["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Staff ID or Password."
        )

    token = generate_session_token(row["id"], row["role"])

    return {
        "success": True,
        "message": "Staff login successful!",
        "token": token,
        "user": {
            "id": row["id"],
            "staff_id": row["staff_id"],
            "name": row["name"],
            "email": row["email"],
            "department": row["department"],
            "role": row["role"]
        }
    }

@router.get("/list")
def get_staff_members():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, staff_id, name, department, role FROM staff ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()

    return {"staff": [dict(r) for r in rows]}
