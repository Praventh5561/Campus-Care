// middleware/auth.js - JWT verification helpers
const jwt = require('jsonwebtoken');
const SECRET = process.env.JWT_SECRET || 'campusscan_super_secret_key_change_this';

function verifyToken(req, res, next) {
  const header = req.headers['authorization'];
  const token = header && header.split(' ')[1];

  if (!token) {
    return res.status(401).json({ success: false, message: 'No token provided' });
  }

  jwt.verify(token, SECRET, (err, decoded) => {
    if (err) {
      return res.status(403).json({ success: false, message: 'Invalid or expired token' });
    }
    req.user = decoded; // { id, role, name, ... }
    next();
  });
}

function requireRole(role) {
  return (req, res, next) => {
    if (!req.user || req.user.role !== role) {
      return res.status(403).json({ success: false, message: `Access restricted to ${role}` });
    }
    next();
  };
}

module.exports = { verifyToken, requireRole, SECRET };
