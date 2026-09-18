import re

# Keyword rules for Smart Urgency & Category Detection
EMERGENCY_KEYWORDS = [
    r"\bleak\b", r"\bburst\b", r"\bpipe\b", r"\bfire\b", r"\bshort circuit\b", 
    r"\bspark\b", r"\bpower cut\b", r"\boutage\b", r"\bhazard\b", r"\bflood\b", r"\bdanger\b"
]

HIGH_KEYWORDS = [
    r"\bbroken\b", r"\bprojector\b", r"\bexam\b", r"\blab\b", r"\bacademics\b", r"\bno water\b"
]

DEPARTMENT_MAP = {
    "Wi-Fi & IT Services": ["Priya Sharma (IT Specialist)", "IT Support"],
    "Electrical & AC": ["Dr. Ramesh Kumar (Maintenance HOD)", "Electrical Dept"],
    "Hostel & Accommodation": ["Hostel Warden Office", "Hostel Admin"],
    "Infrastructure & Furniture": ["Estate Officer", "Maintenance Cell"],
    "Sanitation & Hygiene": ["Housekeeping Supervisor", "Sanitation Cell"],
    "Canteen & Food Quality": ["Canteen Manager", "Food Safety Committee"]
}

def analyze_complaint_text(title: str, description: str, current_urgency: str, current_category: str):
    """
    Intelligent NLP & Keyword analysis engine:
    1. Detects emergency/high urgency keywords.
    2. Suggests appropriate staff/department allocation.
    """
    combined_text = f"{title} {description}".lower()
    
    suggested_urgency = current_urgency
    # 1. Detect Emergency Keywords
    for kw in EMERGENCY_KEYWORDS:
        if re.search(kw, combined_text):
            suggested_urgency = "Emergency"
            break
    
    # 2. Detect High Urgency if not already Emergency
    if suggested_urgency not in ["Emergency", "High"]:
        for kw in HIGH_KEYWORDS:
            if re.search(kw, combined_text):
                suggested_urgency = "High"
                break

    # 3. Suggest Auto-Assigned Department / Staff
    dept_info = DEPARTMENT_MAP.get(current_category, ["Unassigned Staff", "General Cell"])
    suggested_staff = dept_info[0]

    return {
        "urgency": suggested_urgency,
        "suggested_staff": suggested_staff,
        "ai_flags": {
            "urgency_escalated": suggested_urgency != current_urgency,
            "auto_assigned": True
        }
    }
