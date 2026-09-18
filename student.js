// routes/student.js - Student registration & login
const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../db');
const { SECRET, verifyToken } = require('../middleware/auth');

// -------------------- REGISTER --------------------
router.post('/register', async (req, res) => {
  try {
    const { reg_no, name, email, password, department, year, phone } = req.body;

    if (!reg_no || !name || !email || !password || !department) {
      return res.status(400).json({ success: false, message: 'All required fields must be filled' });
    }

    const [existing] = await db.query(
      'SELECT id FROM students WHERE email = ? OR reg_no = ?',
      [email, reg_no]
    );
    if (existing.length > 0) {
      return res.status(409).json({ success: false, message: 'Student already registered with this email or reg no' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    await db.query(
      'INSERT INTO students (reg_no, name, email, password, department, year, phone) VALUES (?,?,?,?,?,?,?)',
      [reg_no, name, email, hashedPassword, department, year || '1', phone || null]
    );

    res.status(201).json({ success: true, message: 'Student registered successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error during registration' });
  }
});

// -------------------- LOGIN --------------------
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ success: false, message: 'Email and password are required' });
    }

    const [rows] = await db.query('SELECT * FROM students WHERE email = ?', [email]);
    if (rows.length === 0) {
      return res.status(401).json({ success: false, message: 'Invalid email or password' });
    }

    const student = rows[0];
    const match = await bcrypt.compare(password, student.password);
    if (!match) {
      return res.status(401).json({ success: false, message: 'Invalid email or password' });
    }

    const token = jwt.sign(
      { id: student.id, role: 'student', name: student.name, department: student.department },
      SECRET,
      { expiresIn: '8h' }
    );

    res.json({
      success: true,
      message: 'Login successful',
      token,
      user: {
        id: student.id,
        reg_no: student.reg_no,
        name: student.name,
        email: student.email,
        department: student.department
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error during login' });
  }
});

// -------------------- GET PROFILE --------------------
router.get('/profile', verifyToken, async (req, res) => {
  try {
    const [rows] = await db.query(
      'SELECT id, reg_no, name, email, department, year, phone FROM students WHERE id = ?',
      [req.user.id]
    );
    if (rows.length === 0) {
      return res.status(404).json({ success: false, message: 'Student not found' });
    }
    res.json({ success: true, student: rows[0] });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
