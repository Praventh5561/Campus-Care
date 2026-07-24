-- =====================================================
-- CampusScan Database Schema
-- Campus Complaint Management System
-- =====================================================

CREATE DATABASE IF NOT EXISTS campus_scan;
USE campus_scan;

-- ---------------------------------------------------
-- Table: students
-- ---------------------------------------------------
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reg_no VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    year VARCHAR(10) DEFAULT '1',
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------
-- Table: staff
-- ---------------------------------------------------
CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    designation VARCHAR(100) DEFAULT 'Staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------
-- Table: complaints
-- ---------------------------------------------------
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    category ENUM('Infrastructure','Hostel','Academic','Ragging','Harassment','Canteen','Other') DEFAULT 'Other',
    location VARCHAR(150),
    status ENUM('Pending','In Progress','Resolved','Rejected') DEFAULT 'Pending',
    priority ENUM('Low','Medium','High') DEFAULT 'Medium',
    is_anonymous BOOLEAN DEFAULT FALSE,
    staff_response TEXT,
    handled_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (handled_by) REFERENCES staff(id) ON DELETE SET NULL
);

-- ---------------------------------------------------
-- Sample seed data (passwords are bcrypt hashes of "password123")
-- ---------------------------------------------------
INSERT INTO staff (staff_id, name, email, password, department, designation)
VALUES
('STF001', 'Dr. Ramesh Kumar', 'ramesh.staff@campus.edu',
 '$2b$10$3euPcmQFCiblsZeEu5s7p.9wVsW1zQU/8Kzz5T0Q4Ho4x8f0KZfr6', 'Administration', 'Grievance Officer');

INSERT INTO students (reg_no, name, email, password, department, year, phone)
VALUES
('CS21001', 'Arun Prasad', 'arun.student@campus.edu',
 '$2b$10$3euPcmQFCiblsZeEu5s7p.9wVsW1zQU/8Kzz5T0Q4Ho4x8f0KZfr6', 'Computer Science', '3', '9876543210');

-- Note: default seed password for both accounts above is: password123
-- (Change immediately after first login in a real deployment)
