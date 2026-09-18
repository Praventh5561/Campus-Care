// db.js - MySQL connection pool for CampusScan
require('dotenv').config();
const mysql = require('mysql2');

const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'campus_scan',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Export a promise-based pool so routes can use async/await
module.exports = pool.promise();
