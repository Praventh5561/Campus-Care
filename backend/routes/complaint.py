from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.db import get_db, generate_ticket_id

router = APIRouter(prefix="/api/complaints", tags=["Complaint Operations"])

class ComplaintCreate(BaseModel):
    student_id: int
    student_name: str
    roll_number: str
    title: str
    category: str
    location: str
    urgency: str
    description: str

class StatusUpdate(BaseModel):
    ticket_id: str
    status: str
    staff_name: str
    staff_role: str
    assigned_staff: Optional[str] = None
    remarks: Optional[str] = ""

@router.post("/submit")
def submit_complaint(complaint: ComplaintCreate):
    conn = get_db()
    cursor = conn.cursor()

    ticket_id = generate_ticket_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO complaints 
        (ticket_id, student_id, student_name, roll_number, title, category, location, urgency, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Submitted', ?, ?)
    """, (ticket_id, complaint.student_id, complaint.student_name, complaint.roll_number, complaint.title, 
          complaint.category, complaint.location, complaint.urgency, complaint.description, now, now))
    
    complaint_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO complaint_history (complaint_id, status_from, status_to, updated_by_role, updated_by_name, comments)
        VALUES (?, NULL, 'Submitted', 'Student', ?, 'Complaint submitted by student.')
    """, (complaint_id, complaint.student_name))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Complaint submitted successfully!",
        "ticket_id": ticket_id
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

    cursor.execute("SELECT id, status, assigned_staff FROM complaints WHERE ticket_id = ?", (update_data.ticket_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Complaint not found.")

    complaint_id = row["id"]
    old_status = row["status"]
    new_status = update_data.status
    assigned_staff = update_data.assigned_staff or row["assigned_staff"]
    remarks = update_data.remarks or ""
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
