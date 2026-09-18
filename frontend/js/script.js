/* ==========================================================================
   CampusCare22 - Real-Time Dashboard, AI Routing & PBKDF2 Auth Client
   ========================================================================== */

const API_BASE = "http://127.0.0.1:8000/api";

function getCurrentUser() {
    const userStr = localStorage.getItem("campusCare22User");
    return userStr ? JSON.parse(userStr) : null;
}

function getAuthToken() {
    return localStorage.getItem("campusCare22Token") || "";
}

function setCurrentSession(user, token) {
    localStorage.setItem("campusCare22User", JSON.stringify(user));
    if (token) localStorage.setItem("campusCare22Token", token);
}

function logout() {
    localStorage.removeItem("campusCare22User");
    localStorage.removeItem("campusCare22Token");
    window.location.href = "index.html";
}

function showAlert(elementId, message, type = "success") {
    const alertEl = document.getElementById(elementId);
    if (!alertEl) return;
    
    alertEl.className = `alert alert-${type}`;
    alertEl.innerText = message;
    alertEl.style.display = "block";
    
    setTimeout(() => {
        alertEl.style.display = "none";
    }, 4000);
}

function checkAuth(requiredRole = null) {
    const user = getCurrentUser();
    if (!user) {
        if (requiredRole === "student") window.location.href = "student-login.html";
        if (requiredRole === "staff") window.location.href = "staff-login.html";
        return null;
    }
    if (requiredRole && user.role !== requiredRole) {
        alert(`Access Denied. Requires ${requiredRole} login.`);
        window.location.href = "index.html";
        return null;
    }
    return user;
}

function getStatusBadge(status) {
    switch (status) {
        case "Submitted":
            return `<span class="badge badge-submitted">Submitted</span>`;
        case "Under Review":
            return `<span class="badge badge-review">Under Review</span>`;
        case "In Progress":
            return `<span class="badge badge-progress">In Progress</span>`;
        case "Resolved":
            return `<span class="badge badge-resolved">Resolved</span>`;
        default:
            return `<span class="badge badge-submitted">${status}</span>`;
    }
}

function getUrgencyBadge(urgency) {
    switch (urgency) {
        case "Low":
            return `<span class="badge badge-low">Low</span>`;
        case "Medium":
            return `<span class="badge badge-medium">Medium</span>`;
        case "High":
            return `<span class="badge badge-high">High</span>`;
        case "Emergency":
            return `<span class="badge badge-emergency">Emergency ⚡</span>`;
        default:
            return `<span class="badge badge-medium">${urgency}</span>`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const userNav = document.getElementById("userNavInfo");
    const user = getCurrentUser();
    if (userNav && user) {
        userNav.innerHTML = `
            <span style="color: var(--text-muted); font-size: 0.9rem; margin-right: 0.5rem;">
                👋 Welcome, <strong>${user.name}</strong> (${user.role.toUpperCase()})
                <span title="Live Real-time Sync Active" style="display:inline-block; width:8px; height:8px; background:#10b981; border-radius:50%; margin-left:6px; animation: pulse 2s infinite;"></span>
            </span>
            <button onclick="logout()" class="btn btn-secondary btn-sm">Logout</button>
        `;
    }

    const studentLoginForm = document.getElementById("studentLoginForm");
    if (studentLoginForm) {
        studentLoginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const roll_number = document.getElementById("roll_number").value;
            const password = document.getElementById("password").value;

            try {
                const res = await fetch(`${API_BASE}/student/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ roll_number, password })
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    setCurrentSession(data.user, data.token);
                    window.location.href = "student-dashboard.html";
                } else {
                    showAlert("loginAlert", data.detail || "Login failed.", "error");
                }
            } catch (err) {
                showAlert("loginAlert", "Cannot connect to server. Is backend running?", "error");
            }
        });
    }

    const studentRegisterForm = document.getElementById("studentRegisterForm");
    if (studentRegisterForm) {
        studentRegisterForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const roll_number = document.getElementById("reg_roll").value;
            const name = document.getElementById("reg_name").value;
            const email = document.getElementById("reg_email").value;
            const password = document.getElementById("reg_pass").value;
            const department = document.getElementById("reg_dept").value;
            const year_of_study = parseInt(document.getElementById("reg_year").value);

            try {
                const res = await fetch(`${API_BASE}/student/register`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ roll_number, name, email, password, department, year_of_study })
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    setCurrentSession(data.user, data.token);
                    alert("Registration successful! Redirecting to Dashboard...");
                    window.location.href = "student-dashboard.html";
                } else {
                    showAlert("regAlert", data.detail || "Registration failed.", "error");
                }
            } catch (err) {
                showAlert("regAlert", "Cannot connect to backend server.", "error");
            }
        });
    }

    const staffLoginForm = document.getElementById("staffLoginForm");
    if (staffLoginForm) {
        staffLoginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const staff_id = document.getElementById("staff_id").value;
            const password = document.getElementById("staff_password").value;

            try {
                const res = await fetch(`${API_BASE}/staff/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ staff_id, password })
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    setCurrentSession(data.user, data.token);
                    window.location.href = "staff-dashboard.html";
                } else {
                    showAlert("staffAlert", data.detail || "Invalid Staff Credentials.", "error");
                }
            } catch (err) {
                showAlert("staffAlert", "Cannot connect to backend server.", "error");
            }
        });
    }

    const complaintForm = document.getElementById("complaintForm");
    if (complaintForm) {
        const studentUser = checkAuth("student");
        if (studentUser) {
            document.getElementById("student_name_disp").value = `${studentUser.name} (${studentUser.roll_number})`;
        }

        complaintForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            if (!studentUser) return;

            const formData = new FormData();
            formData.append("student_id", studentUser.id);
            formData.append("student_name", studentUser.name);
            formData.append("roll_number", studentUser.roll_number);
            formData.append("title", document.getElementById("title").value);
            formData.append("category", document.getElementById("category").value);
            formData.append("location", document.getElementById("location").value);
            formData.append("urgency", document.getElementById("urgency").value);
            formData.append("description", document.getElementById("description").value);

            const fileInput = document.getElementById("image_file");
            if (fileInput && fileInput.files[0]) {
                formData.append("image", fileInput.files[0]);
            }

            try {
                const res = await fetch(`${API_BASE}/complaints/submit`, {
                    method: "POST",
                    headers: { "Authorization": `Bearer ${getAuthToken()}` },
                    body: formData
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    let alertMsg = `🎉 Complaint Registered! Ticket ID: ${data.ticket_id}`;
                    if (data.urgency === "Emergency") alertMsg += "\n⚡ AI System Escalated Urgency to EMERGENCY!";
                    alert(alertMsg);
                    window.location.href = `status.html?ticket=${data.ticket_id}`;
                } else {
                    showAlert("formAlert", data.detail || "Submission failed.", "error");
                }
            } catch (err) {
                showAlert("formAlert", "Server connection error.", "error");
            }
        });
    }

    // Real-Time Polling setup for Student Dashboard
    if (document.getElementById("studentComplaintsTable")) {
        const studentUser = checkAuth("student");
        if (studentUser) {
            loadStudentDashboard(studentUser.id);
            // Real-Time Auto Refresh every 15 seconds
            setInterval(() => loadStudentDashboard(studentUser.id), 15000);
        }
    }

    // Real-Time Polling setup for Staff Control Center
    if (document.getElementById("staffComplaintsTable")) {
        const staffUser = checkAuth("staff");
        if (staffUser) {
            loadStaffDashboard();
            // Real-Time Auto Refresh every 15 seconds
            setInterval(() => loadStaffDashboard(), 15000);
        }
    }

    if (document.getElementById("statusSearchContainer")) {
        const urlParams = new URLSearchParams(window.location.search);
        const ticketParam = urlParams.get("ticket");
        if (ticketParam) {
            document.getElementById("ticketSearchInput").value = ticketParam;
            fetchTicketDetails(ticketParam);
        }

        document.getElementById("ticketSearchBtn").addEventListener("click", () => {
            const ticketId = document.getElementById("ticketSearchInput").value.trim();
            if (ticketId) fetchTicketDetails(ticketId);
        });
    }
});

async function loadStudentDashboard(studentId) {
    try {
        const res = await fetch(`${API_BASE}/complaints/student/${studentId}`, {
            headers: { "Authorization": `Bearer ${getAuthToken()}` }
        });
        const data = await res.json();
        const complaints = data.complaints || [];

        const tableBody = document.getElementById("studentComplaintsTable");
        if (!tableBody) return;

        if (complaints.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No complaints registered yet. Click "File New Complaint" to create one.</td></tr>`;
            return;
        }

        tableBody.innerHTML = complaints.map(c => `
            <tr>
                <td><strong><a href="status.html?ticket=${c.ticket_id}">${c.ticket_id}</a></strong></td>
                <td>
                    ${c.title}
                    ${c.image_path ? '<span style="font-size:0.75rem; background:rgba(99,102,241,0.2); color:#a5b4fc; padding:2px 6px; border-radius:4px; margin-left:6px;">📷 Photo</span>' : ''}
                </td>
                <td>${c.category}</td>
                <td>${getUrgencyBadge(c.urgency)}</td>
                <td>${getStatusBadge(c.status)}</td>
                <td>
                    <a href="status.html?ticket=${c.ticket_id}" class="btn btn-secondary btn-sm">Track Progress</a>
                </td>
            </tr>
        `).join("");

        document.getElementById("myTotalCount").innerText = complaints.length;
        document.getElementById("myPendingCount").innerText = complaints.filter(c => c.status === "Submitted" || c.status === "Under Review").length;
        document.getElementById("myResolvedCount").innerText = complaints.filter(c => c.status === "Resolved").length;
    } catch (err) {
        console.error("Error loading student dashboard:", err);
    }
}

async function loadStaffDashboard() {
    try {
        const statsRes = await fetch(`${API_BASE}/complaints/metrics/stats`);
        const stats = await statsRes.json();
        document.getElementById("totalCount").innerText = stats.total || 0;
        document.getElementById("pendingCount").innerText = stats.pending || 0;
        document.getElementById("progressCount").innerText = stats.in_progress || 0;
        document.getElementById("resolvedCount").innerText = stats.resolved || 0;

        fetchStaffComplaints();
    } catch (err) {
        console.error("Error loading staff stats:", err);
    }
}

async function fetchStaffComplaints() {
    const statusFilter = document.getElementById("statusFilter") ? document.getElementById("statusFilter").value : "All";
    const categoryFilter = document.getElementById("categoryFilter") ? document.getElementById("categoryFilter").value : "All";
    const search = document.getElementById("staffSearchInput") ? document.getElementById("staffSearchInput").value.trim() : "";

    const queryParams = new URLSearchParams({
        status_filter: statusFilter,
        category_filter: categoryFilter,
        search: search
    });

    try {
        const res = await fetch(`${API_BASE}/complaints/all?${queryParams}`, {
            headers: { "Authorization": `Bearer ${getAuthToken()}` }
        });
        const data = await res.json();
        const complaints = data.complaints || [];

        const tableBody = document.getElementById("staffComplaintsTable");
        if (!tableBody) return;

        if (complaints.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No complaints match current filters.</td></tr>`;
            return;
        }

        tableBody.innerHTML = complaints.map(c => `
            <tr>
                <td><strong><a href="status.html?ticket=${c.ticket_id}">${c.ticket_id}</a></strong></td>
                <td>${c.student_name} (${c.roll_number})</td>
                <td>
                    ${c.title}
                    ${c.image_path ? '<span style="font-size:0.75rem; background:rgba(99,102,241,0.2); color:#a5b4fc; padding:2px 6px; border-radius:4px; margin-left:6px;">📷 Photo</span>' : ''}
                </td>
                <td><small>${c.category}<br><span style="color:var(--text-dim);">${c.location}</span></small></td>
                <td>${getUrgencyBadge(c.urgency)}</td>
                <td>${getStatusBadge(c.status)}</td>
                <td><small>${c.assigned_staff || 'Unassigned'}</small></td>
                <td>
                    <button onclick="openUpdateModal('${c.ticket_id}', '${c.status}', '${c.assigned_staff}')" class="btn btn-primary btn-sm">Update</button>
                </td>
            </tr>
        `).join("");
    } catch (err) {
        console.error("Error fetching staff complaints:", err);
    }
}

async function fetchTicketDetails(ticketId) {
    const detailsContainer = document.getElementById("ticketResultContainer");
    const errorAlert = document.getElementById("searchAlert");

    try {
        const res = await fetch(`${API_BASE}/complaints/ticket/${ticketId}`);
        const data = await res.json();

        if (!res.ok || !data.complaint) {
            if (errorAlert) {
                errorAlert.innerText = `Ticket '${ticketId}' not found. Please check ticket ID format (e.g. CC22-2026-8941).`;
                errorAlert.style.display = "block";
            }
            if (detailsContainer) detailsContainer.style.display = "none";
            return;
        }

        if (errorAlert) errorAlert.style.display = "none";
        if (detailsContainer) detailsContainer.style.display = "block";

        const c = data.complaint;
        document.getElementById("ticketHeading").innerText = `Ticket: ${c.ticket_id}`;
        document.getElementById("ticketTitle").innerText = c.title;
        document.getElementById("ticketCategory").innerText = c.category;
        document.getElementById("ticketLocation").innerText = c.location;
        document.getElementById("ticketUrgency").innerHTML = getUrgencyBadge(c.urgency);
        document.getElementById("ticketStatus").innerHTML = getStatusBadge(c.status);
        document.getElementById("ticketStudent").innerText = `${c.student_name} (${c.roll_number})`;
        document.getElementById("ticketDesc").innerText = c.description;
        document.getElementById("ticketAssigned").innerText = c.assigned_staff || "Awaiting Staff Assignment";
        document.getElementById("ticketRemarks").innerText = c.staff_remarks || "No remarks added yet.";

        const imgContainer = document.getElementById("ticketImagePreview");
        if (imgContainer) {
            if (c.image_path) {
                imgContainer.innerHTML = `
                    <small style="color: var(--text-dim); text-transform: uppercase; font-weight: 700;">Attached Photo Evidence</small><br>
                    <a href="${c.image_path}" target="_blank">
                        <img src="${c.image_path}" alt="Issue Photo" style="max-width: 100%; max-height: 250px; border-radius: var(--radius-md); border: 1px solid var(--border-glass-light); margin-top: 0.5rem; object-fit: cover;">
                    </a>
                `;
                imgContainer.style.display = "block";
            } else {
                imgContainer.style.display = "none";
            }
        }

        const history = c.history || [];
        const timelineEl = document.getElementById("ticketTimeline");
        if (timelineEl) {
            timelineEl.innerHTML = history.map((item, index) => `
                <div class="timeline-item ${index === history.length - 1 ? 'active' : ''}">
                    <div class="timeline-point">${index === history.length - 1 ? '📌' : '✓'}</div>
                    <div class="timeline-content">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>Status: ${item.status_to}</strong>
                            <small style="color:var(--text-dim);">${item.timestamp}</small>
                        </div>
                        <p style="font-size:0.9rem; color:var(--text-muted); margin-top:0.3rem;">
                            Updated by: <strong>${item.updated_by_name}</strong> (${item.updated_by_role})
                        </p>
                        ${item.comments ? `<p style="font-size:0.88rem; color:#cbd5e1; margin-top:0.3rem; font-style:italic;">"${item.comments}"</p>` : ''}
                    </div>
                </div>
            `).join("");
        }
    } catch (err) {
        if (errorAlert) {
            errorAlert.innerText = "Error connecting to backend server.";
            errorAlert.style.display = "block";
        }
    }
}

let currentEditingTicket = null;

function openUpdateModal(ticketId, currentStatus, currentStaff) {
    currentEditingTicket = ticketId;
    document.getElementById("modalTicketId").innerText = ticketId;
    document.getElementById("updateStatusSelect").value = currentStatus;
    document.getElementById("updateStaffInput").value = currentStaff !== "Unassigned" ? currentStaff : "";
    document.getElementById("updateRemarks").value = "";
    document.getElementById("statusModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("statusModal").style.display = "none";
}

async function submitStatusUpdate() {
    const staffUser = getCurrentUser();
    if (!staffUser || !currentEditingTicket) return;

    const payload = {
        ticket_id: currentEditingTicket,
        status: document.getElementById("updateStatusSelect").value,
        staff_name: staffUser.name,
        staff_role: staffUser.role,
        assigned_staff: document.getElementById("updateStaffInput").value || staffUser.name,
        remarks: document.getElementById("updateRemarks").value
    };

    try {
        const res = await fetch(`${API_BASE}/complaints/update-status`, {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getAuthToken()}`
            },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok && data.success) {
            alert(data.message);
            closeModal();
            loadStaffDashboard();
        } else {
            alert(data.detail || "Update failed.");
        }
    } catch (err) {
        alert("Server error occurred.");
    }
}
