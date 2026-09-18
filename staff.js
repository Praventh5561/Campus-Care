// routes/staff.js - Staff login & stats
const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../db');
const { SECRET, verifyToken, requireRole } = require('../middleware/auth');

// -------------------- LOGIN --------------------
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ success: false, message: 'Email and password are required' });
    }

    const [rows] = await db.query('SELECT * FROM staff WHERE email = ?', [email]);
    if (rows.length === 0) {
      return res.status(401).json({ success: false, message: 'Invalid email or password' });
    }

    const staff = rows[0];
    const match = await bcrypt.compare(password, staff.password);
    if (!match) {
      return res.status(401).json({ success: false, message: 'Invalid email or password' });
    }

    const token = jwt.sign(
      { id: staff.id, role: 'staff', name: staff.name, department: staff.department },
      SECRET,
      { expiresIn: '8h' }
    );

    res.json({
      success: true,
      message: 'Login successful',
      token,
      user: {
        id: staff.id,
        staff_id: staff.staff_id,
        name: staff.name,
        email: staff.email,
        department: staff.department,
        designation: staff.designation
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error during login' });
  }
});

// -------------------- DASHBOARD STATS --------------------
router.get('/stats', verifyToken, requireRole('staff'), async (req, res) => {
  try {
    const [[{ total }]] = await db.query('SELECT COUNT(*) AS total FROM complaints');
    const [[{ pending }]] = await db.query("SELECT COUNT(*) AS pending FROM complaints WHERE status='Pending'");
    const [[{ inProgress }]] = await db.query("SELECT COUNT(*) AS inProgress FROM complaints WHERE status='In Progress'");
    const [[{ resolved }]] = await db.query("SELECT COUNT(*) AS resolved FROM complaints WHERE status='Resolved'");

    res.json({ success: true, stats: { total, pending, inProgress, resolved } });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error fetching stats' });
  }
});

module.exports = router;
