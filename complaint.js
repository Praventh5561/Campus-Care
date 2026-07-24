// routes/complaint.js - Complaint CRUD operations
const express = require('express');
const router = express.Router();
const db = require('../db');
const { verifyToken, requireRole } = require('../middleware/auth');

// -------------------- CREATE COMPLAINT (student) --------------------
router.post('/add', verifyToken, requireRole('student'), async (req, res) => {
  try {
    const { title, description, category, location, priority, is_anonymous } = req.body;

    if (!title || !description) {
      return res.status(400).json({ success: false, message: 'Title and description are required' });
    }

    const [result] = await db.query(
      `INSERT INTO complaints (student_id, title, description, category, location, priority, is_anonymous)
       VALUES (?,?,?,?,?,?,?)`,
      [
        req.user.id,
        title,
        description,
        category || 'Other',
        location || null,
        priority || 'Medium',
        is_anonymous ? 1 : 0
      ]
    );

    res.status(201).json({ success: true, message: 'Complaint submitted successfully', complaintId: result.insertId });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error submitting complaint' });
  }
});

// -------------------- GET MY COMPLAINTS (student) --------------------
router.get('/my', verifyToken, requireRole('student'), async (req, res) => {
  try {
    const [rows] = await db.query(
      'SELECT * FROM complaints WHERE student_id = ? ORDER BY created_at DESC',
      [req.user.id]
    );
    res.json({ success: true, complaints: rows });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error fetching complaints' });
  }
});

// -------------------- GET ALL COMPLAINTS (staff) --------------------
router.get('/all', verifyToken, requireRole('staff'), async (req, res) => {
  try {
    const { status, category } = req.query;
    let query = `
      SELECT c.*,
             CASE WHEN c.is_anonymous = 1 THEN 'Anonymous' ELSE s.name END AS student_name,
             s.reg_no, s.department AS student_department
      FROM complaints c
      JOIN students s ON c.student_id = s.id
      WHERE 1=1`;
    const params = [];

    if (status) {
      query += ' AND c.status = ?';
      params.push(status);
    }
    if (category) {
      query += ' AND c.category = ?';
      params.push(category);
    }
    query += ' ORDER BY c.created_at DESC';

    const [rows] = await db.query(query, params);
    res.json({ success: true, complaints: rows });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error fetching complaints' });
  }
});

// -------------------- UPDATE COMPLAINT STATUS (staff) --------------------
router.put('/update/:id', verifyToken, requireRole('staff'), async (req, res) => {
  try {
    const { status, staff_response } = req.body;
    const { id } = req.params;

    const validStatuses = ['Pending', 'In Progress', 'Resolved', 'Rejected'];
    if (status && !validStatuses.includes(status)) {
      return res.status(400).json({ success: false, message: 'Invalid status value' });
    }

    await db.query(
      `UPDATE complaints
       SET status = COALESCE(?, status),
           staff_response = COALESCE(?, staff_response),
           handled_by = ?
       WHERE id = ?`,
      [status || null, staff_response || null, req.user.id, id]
    );

    res.json({ success: true, message: 'Complaint updated successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error updating complaint' });
  }
});

// -------------------- GET SINGLE COMPLAINT (student or staff) --------------------
router.get('/:id', verifyToken, async (req, res) => {
  try {
    const [rows] = await db.query(
      `SELECT c.*,
              CASE WHEN c.is_anonymous = 1 THEN 'Anonymous' ELSE s.name END AS student_name
       FROM complaints c JOIN students s ON c.student_id = s.id
       WHERE c.id = ?`,
      [req.params.id]
    );
    if (rows.length === 0) {
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    const complaint = rows[0];
    // students may only view their own complaint
    if (req.user.role === 'student' && complaint.student_id !== req.user.id) {
      return res.status(403).json({ success: false, message: 'Access denied' });
    }

    res.json({ success: true, complaint });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error fetching complaint' });
  }
});

module.exports = router;
