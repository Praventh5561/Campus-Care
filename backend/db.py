import sqlite3
import os
import random
from datetime import datetime

DB_PATH = "/tmp/campus_care22.db" if os.environ.get("VERCEL") else os.path.join(os.path.dirname(__file__), "campus_care22.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite tables and seed records if empty."""
    conn = get_db()
    cursor = conn.cursor()

    # Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_number TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        department TEXT NOT NULL,
        year_of_study INTEGER DEFAULT 1,
        phone TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Staff Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        department TEXT NOT NULL,
        role TEXT DEFAULT 'Staff',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Complaints Table (With image_path support)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        student_id INTEGER NOT NULL,
        student_name TEXT NOT NULL,
        roll_number TEXT NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        location TEXT NOT NULL,
        urgency TEXT DEFAULT 'Medium',
        description TEXT NOT NULL,
        image_path TEXT DEFAULT '',
        status TEXT DEFAULT 'Submitted',
        assigned_staff TEXT DEFAULT 'Unassigned',
        staff_remarks TEXT DEFAULT '',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id)
    );
    """)

    # Check if image_path column exists (for existing DB migration)
    cursor.execute("PRAGMA table_info(complaints)")
    columns = [col[1] for col in cursor.fetchall()]
    if "image_path" not in columns:
        cursor.execute("ALTER TABLE complaints ADD COLUMN image_path TEXT DEFAULT ''")

    # Complaint History Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaint_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id INTEGER NOT NULL,
        status_from TEXT,
        status_to TEXT NOT NULL,
        updated_by_role TEXT NOT NULL,
        updated_by_name TEXT NOT NULL,
        comments TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (complaint_id) REFERENCES complaints(id)
    );
    """)

    # Seed Default Staff if empty
    cursor.execute("SELECT COUNT(*) FROM staff")
    if cursor.fetchone()[0] == 0:
        default_staff = [
            ('STF101', 'Dr. Ramesh Kumar', 'ramesh.staff@college.edu', 'staff123', 'Maintenance', 'HOD'),
            ('STF102', 'Priya Sharma', 'priya.it@college.edu', 'staff123', 'IT Support', 'Staff'),
            ('ADM001', 'Campus Admin', 'admin@college.edu', 'admin123', 'Administration', 'Admin')
        ]
        cursor.executemany("INSERT INTO staff (staff_id, name, email, password, department, role) VALUES (?, ?, ?, ?, ?, ?)", default_staff)

    # Seed Default Student if empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        default_students = [
            ('21CS045', 'Arun V', 'arun.21cs@college.edu', 'student123', 'Computer Science', 3, '9876543210'),
            ('22EC012', 'Sneha R', 'sneha.22ec@college.edu', 'student123', 'Electronics & Comm', 2, '9123456780')
        ]
        cursor.executemany("INSERT INTO students (roll_number, name, email, password, department, year_of_study, phone) VALUES (?, ?, ?, ?, ?, ?, ?)", default_students)

    # Seed Sample Complaints if empty
    cursor.execute("SELECT COUNT(*) FROM complaints")
    if cursor.fetchone()[0] == 0:
        sample_complaints = [
            ('CC22-2026-8941', 1, 'Arun V', '21CS045', 'Lab 3 Projector Defective', 'Infrastructure & Furniture', 'Main Block - CS Lab 3', 'High', 'The main ceiling projector flickers constantly during lectures.', '', 'Under Review', 'Priya Sharma', 'Technician assigned for hardware inspection.'),
            ('CC22-2026-3109', 2, 'Sneha R', '22EC012', 'Hostel Block B Hot Water Outage', 'Hostel & Accommodation', 'Hostel B - 3rd Floor', 'Emergency', 'Solar heater supply pipe leaking, no warm water since morning.', '', 'Submitted', 'Unassigned', 'Awaiting staff allocation.')
        ]
        cursor.executemany("INSERT INTO complaints (ticket_id, student_id, student_name, roll_number, title, category, location, urgency, description, image_path, status, assigned_staff, staff_remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_complaints)

        cursor.execute("INSERT INTO complaint_history (complaint_id, status_from, status_to, updated_by_role, updated_by_name, comments) VALUES (1, 'Submitted', 'Under Review', 'Staff', 'Priya Sharma', 'Assigned technician to inspect Lab 3 projector hardware.')")

    conn.commit()
    conn.close()

def generate_ticket_id():
    year = datetime.now().year
    rand_num = random.randint(1000, 9999)
    return f"CC22-{year}-{rand_num}"
