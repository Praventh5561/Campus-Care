import os
import shutil
from fastapi import APIRouter, HTTPException, Query, Form, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.db import get_db, generate_ticket_id
from backend.notifications import send_complaint_confirmation, send_status_update_notification

router = APIRouter(prefix="/api/complaints", tags=["Complaint Operations"])

# Upload directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

class StatusUpdate(BaseModel):
    ticket_id: str
    status: str
    staff_name: str
    staff_role: str
    assigned_staff: Optional[str] = None
    remarks: Optional[str] = ""

@router.post("/submit")
async def submit_complaint(
    student_id: int = Form(...),
    student_name: str = Form(...),
    roll_number: str = Form(...),
    title: str = Form(...),
    category: str = Form(...),
    location: str = Form(...),
    urgency: str = Form(...),
    description: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    conn = get_db()
    cursor = conn.cursor()

    ticket_id = generate_ticket_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    image_path_str = ""
    if image and image.filename:
        file_extension = os.path.splitext(image.filename)[1]
        saved_filename = f"{ticket_id}_{int(datetime.now().timestamp())}{file_extension}"
        destination = os.path.join(UPLOAD_DIR, saved_filename)
        
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_path_str = f"uploads/{saved_filename}"

    cursor.execute("""
        INSERT INTO complaints 
        (ticket_id, student_id, student_name, roll_number, title, category, location, urgency, description, image_path, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Submitted', ?, ?)
    """, (ticket_id, student_id, student_name, roll_number, title, 
          category, location, urgency, description, image_path_str, now, now))
    
    complaint_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO complaint_history (complaint_id, status_from, status_to, updated_by_role, updated_by_name, comments)
        VALUES (?, NULL, 'Submitted', 'Student', ?, 'Complaint submitted with issue details.')
    """, (complaint_id, student_name))

    # Fetch student email for confirmation notification
    cursor.execute("SELECT email FROM students WHERE id = ?", (student_id,))
    student_row = cursor.fetchone()
    student_email = student_row["email"] if student_row else f"{roll_number.lower()}@college.edu"

    conn.commit()
    conn.close()

    # Trigger Automated Confirmation Notification
    send_complaint_confirmation(student_email, student_name, ticket_id, title)

    return {
        "success": True,
        "message": "Complaint submitted successfully!",
        "ticket_id": ticket_id,
        "image_path": image_path_str
    }

@router.get("/student/{student_id}")
def get_student_complaints(student_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE student_id = ? ORDER BY id DESC", (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return {"complaints": [dict(r) for r in rows]}

@router.get("/all")
def get_all_complaints(
    status_filter: Optional[str] = Query(None),
    category_filter: Optional[str] = Query(None),
    urgency_filter: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM complaints WHERE 1=1"
    params = []

    if status_filter and status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
    
    if category_filter and category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)

    if urgency_filter and urgency_filter != "All":
        query += " AND urgency = ?"
        params.append(urgency_filter)

    if search:
        query += " AND (ticket_id LIKE ? OR title LIKE ? OR location LIKE ? OR student_name LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term, term])

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return {"complaints": [dict(r) for r in rows]}

@router.get("/ticket/{ticket_id}")
def get_complaint_by_ticket(ticket_id: str):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM complaints WHERE ticket_id = ?", (ticket_id,))
    complaint = cursor.fetchone()

    if not complaint:
        conn.close()
        raise HTTPException(status_code=404, detail="Complaint ticket not found.")

    complaint_dict = dict(complaint)

    cursor.execute("""
        SELECT status_from, status_to, updated_by_role, updated_by_name, comments, timestamp 
        FROM complaint_history 
        WHERE complaint_id = ? 
        ORDER BY id ASC
    """, (complaint_dict["id"],))
    history_rows = cursor.fetchall()
    
    conn.close()
    complaint_dict["history"] = [dict(h) for h in history_rows]

    return {"complaint": complaint_dict}

@router.put("/update-status")
def update_complaint_status(update_data: StatusUpdate):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id, c.status, c.assigned_staff, c.student_id, c.student_name, s.email as student_email
        FROM complaints c
        LEFT JOIN students s ON c.student_id = s.id
        WHERE c.ticket_id = ?
    """, (update_data.ticket_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Complaint not found.")

    complaint_id = row["id"]
    old_status = row["status"]
    new_status = update_data.status
    assigned_staff = update_data.assigned_staff or row["assigned_staff"]
    remarks = update_data.remarks or ""
    student_name = row["student_name"]
    student_email = row["student_email"] or "student@college.edu"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE complaints 
        SET status = ?, assigned_staff = ?, staff_remarks = ?, updated_at = ?
        WHERE id = ?
    """, (new_status, assigned_staff, remarks, now, complaint_id))

    comment_text = remarks if remarks else f"Status updated to {new_status} by {update_data.staff_name}"
    cursor.execute("""
        INSERT INTO complaint_history (complaint_id, status_from, status_to, updated_by_role, updated_by_name, comments)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (complaint_id, old_status, new_status, update_data.staff_role, update_data.staff_name, comment_text))

    conn.commit()
    conn.close()

    # Trigger Automated Email Notification on Status Update
    send_status_update_notification(
        student_email=student_email,
        student_name=student_name,
        ticket_id=update_data.ticket_id,
        new_status=new_status,
        remarks=remarks,
        updated_by=f"{update_data.staff_name} ({update_data.staff_role})"
    )

    return {
        "success": True,
        "message": f"Complaint {update_data.ticket_id} updated to '{new_status}' successfully!"
    }

@router.get("/metrics/stats")
def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Submitted'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Under Review' OR status = 'In Progress'")
    in_progress = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'")
    resolved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE urgency = 'Emergency'")
    emergency = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "emergency": emergency
    }
