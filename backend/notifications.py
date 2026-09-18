import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email Configuration (Set environment variables or use console log fallback)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply.campuscare22@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

def send_complaint_confirmation(student_email: str, student_name: str, ticket_id: str, title: str):
    """Sends a confirmation notification to the student upon complaint submission."""
    subject = f"CampusCare22: Complaint Registered - Ticket #{ticket_id}"
    body = f"""Dear {student_name},

Your grievance has been successfully lodged in CampusCare22.

Ticket Details:
- Ticket ID: {ticket_id}
- Subject: {title}
- Status: Submitted
- Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

You can track your real-time complaint status at:
http://127.0.0.1:8000/static/status.html?ticket={ticket_id}

Regards,
CampusCare22 Support Team
"""
    _dispatch_email(student_email, subject, body)

def send_status_update_notification(student_email: str, student_name: str, ticket_id: str, new_status: str, remarks: str, updated_by: str):
    """Sends an automated email notification when staff updates ticket status."""
    subject = f"CampusCare22: Ticket #{ticket_id} Status Updated to '{new_status}'"
    body = f"""Dear {student_name},

Your campus complaint (Ticket #{ticket_id}) status has been updated.

Update Details:
- New Status: {new_status}
- Updated By: {updated_by}
- Remarks / Resolution Note: {remarks if remarks else 'No additional notes.'}
- Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Track the full resolution progress timeline here:
http://127.0.0.1:8000/static/status.html?ticket={ticket_id}

Regards,
CampusCare22 Maintenance Cell
"""
    _dispatch_email(student_email, subject, body)

def _dispatch_email(recipient_email: str, subject: str, body: str):
    """Dispatches email via SMTP if configured, or logs formatted notification event."""
    print(f"\n=======================================================")
    print(f"📧 [NOTIFICATION DISPATCHED] To: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Content:\n{body}")
    print(f"=======================================================\n")

    if SENDER_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"✓ Email successfully delivered to {recipient_email}")
        except Exception as e:
            print(f"⚠️ SMTP Delivery Warning: {e}")
