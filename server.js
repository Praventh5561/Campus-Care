// server.js - CampusScan backend entry point
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const studentRoutes = require('./routes/student');
const staffRoutes = require('./routes/staff');
const complaintRoutes = require('./routes/complaint');

const app = express();
const PORT = process.env.PORT || 5000;

// -------------------- MIDDLEWARE --------------------
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve the frontend as static files
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// -------------------- API ROUTES --------------------
app.use('/api/student', studentRoutes);
app.use('/api/staff', staffRoutes);
app.use('/api/complaint', complaintRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ success: true, message: 'CampusScan API is running' });
});

// Fallback: serve index.html for any unmatched non-API route
app.get('*', (req, res, next) => {
  if (req.path.startsWith('/api')) return next();
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'));
});

// -------------------- ERROR HANDLER --------------------
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ success: false, message: 'Something went wrong on the server' });
});

app.listen(PORT, () => {
  console.log(`CampusScan server running at http://localhost:${PORT}`);
});
