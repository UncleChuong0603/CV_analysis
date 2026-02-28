from __future__ import annotations

GOOGLE_FORM_BASE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfj7dsIMMWBUCSxss7KLGN-dPaANW5awtX44Er0lFmr3VorBg/viewform"

# Mapping derived from the target form structure.
# Keys here are the app/candidate fields; values are Google Form entry IDs.
FORM_FIELD_MAPPING = {
    "candidate_full_name": "entry.1048297419",
    "position_referred": "entry.2096764674",
    "candidate_team": "entry.1625861106",
    "candidate_email": "entry.1159734209",
    "candidate_phone": "entry.1029247077",
    "english_speaking_level": "entry.1577761297",
    "overall_assessment": "entry.1668207262",
    "cv_drive_link": "entry.366282983",
}

# Fixed options from form; can be preselected by recruiter.
FORM_OPTION_ENTRIES = {
    "project_referred": "entry.1457734049",
    "shift_schedule": "entry.310100462",
    "onboard_timeline": "entry.1340860074",
}

PROJECT_OPTIONS = ["O365", "Azure", "Dynamics 365", "Windows Commercial", "Back office"]
SHIFT_OPTIONS = [
    "Can work all assigned shifts (rotating morning, afternoon, and night shifts)",
    "Can only work fixed daytime shifts",
    "Can only work fixed night shifts",
]
ONBOARD_OPTIONS = [
    "ASAP after interview pass",
    "≤30 days from interview pass",
    ">30 days from interview pass",
]
