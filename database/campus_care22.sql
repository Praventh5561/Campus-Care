-- CampusCare22 - College Grievance & Issue Management System Schema
-- Database: campus_care22

CREATE DATABASE IF NOT EXISTS campus_care22;
USE campus_care22;

-- 1. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(50) NOT NULL,
    year_of_study INT NOT NULL DEFAULT 1,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Staff Table
CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(50) NOT NULL,
    role VARCHAR(30) DEFAULT 'Staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Categories Table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    assigned_dept VARCHAR(50)
);

-- 5. Complaints Table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id VARCHAR(30) NOT NULL UNIQUE,
    student_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    urgency VARCHAR(20) DEFAULT 'Medium',
    description TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'Submitted',
    assigned_staff_id INT DEFAULT NULL,
    staff_remarks TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_staff_id) REFERENCES staff(id) ON DELETE SET NULL
);

-- 6. Complaint Audit Logs / History Table
CREATE TABLE IF NOT EXISTS complaint_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    status_from VARCHAR(30),
    status_to VARCHAR(30) NOT NULL,
    updated_by_role VARCHAR(20) NOT NULL,
    updated_by_name VARCHAR(100) NOT NULL,
    comments TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
);

-- Seed Data: Categories
INSERT INTO categories (name, description, assigned_dept) VALUES
('Hostel & Accommodation', 'Issues related to rooms, plumbing, clean water, and mess', 'Hostel Dept'),
('Infrastructure & Furniture', 'Broken desks, lab chairs, doors, windows, lighting', 'Estate Office'),
('Wi-Fi & IT Services', 'Network outage, portal access, lab PC malfunctions', 'IT Support'),
('Academics & Library', 'Classroom audio, projector, books, syllabus queries', 'Academic Cell'),
('Electrical & AC', 'Power cuts, ceiling fans, AC cooling, switchboard hazards', 'Maintenance'),
('Sanitation & Hygiene', 'Washroom cleanliness, trash collection, campus grounds', 'Housekeeping'),
('Canteen & Food Quality', 'Hygiene standards, food quality, pricing issues', 'Canteen Committee')
ON DUPLICATE KEY UPDATE name=name;

-- Seed Data: Staff (Password: staff123 / admin123)
INSERT INTO staff (staff_id, name, email, password, department, role) VALUES
('STF101', 'Dr. Ramesh Kumar', 'ramesh.staff@college.edu', 'staff123', 'Maintenance', 'HOD'),
('STF102', 'Priya Sharma', 'priya.it@college.edu', 'staff123', 'IT Support', 'Staff'),
('ADM001', 'Campus Admin', 'admin@college.edu', 'admin123', 'Administration', 'Admin')
ON DUPLICATE KEY UPDATE staff_id=staff_id;

-- Seed Data: Student (Password: student123)
INSERT INTO students (roll_number, name, email, password, department, year_of_study, phone) VALUES
('21CS045', 'Arun V', 'arun.21cs@college.edu', 'student123', 'Computer Science', 3, '9876543210')
ON DUPLICATE KEY UPDATE roll_number=roll_number;

-- Seed Data: Sample Complaint
INSERT INTO complaints (ticket_id, student_id, title, category, location, urgency, description, status) VALUES
('CC22-2026-8941', 1, 'Lab 3 Projector Defective', 'Infrastructure & Furniture', 'Main Block - CS Lab 3', 'High', 'The main ceiling projector flickers constantly during lectures and has color distortion.', 'Under Review');

INSERT INTO complaint_history (complaint_id, status_from, status_to, updated_by_role, updated_by_name, comments) VALUES
(1, 'Submitted', 'Under Review', 'Staff', 'Priya Sharma', 'Assigned technician to inspect Lab 3 projector hardware.');
