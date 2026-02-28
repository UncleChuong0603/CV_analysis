from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from cv_parser import extract_candidate_profile, extract_text_from_pdf
from form_config import (
    FORM_FIELD_MAPPING,
    FORM_OPTION_ENTRIES,
    GOOGLE_FORM_BASE_URL,
    ONBOARD_OPTIONS,
    PROJECT_OPTIONS,
    SHIFT_OPTIONS,
)
from google_form import build_prefilled_url


st.set_page_config(page_title="CV → Company Google Form", layout="wide")
st.title("CV PDF → Company Google Form Prefill")
st.caption("Configured for form: 1FAIpQLSfj7dsIMMWBUCSxss7KLGN-dPaANW5awtX44Er0lFmr3VorBg")

uploaded_pdf = st.file_uploader("Upload candidate CV (PDF)", type=["pdf"])

if uploaded_pdf:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        temp_pdf_path = Path(tmp.name)

    raw_text = extract_text_from_pdf(temp_pdf_path)
    profile = extract_candidate_profile(raw_text).to_dict()

    st.subheader("Candidate fields extracted from CV")
    edited_profile: dict[str, str] = {}

    editable_fields = [
        "candidate_full_name",
        "position_referred",
        "candidate_team",
        "candidate_email",
        "candidate_phone",
        "english_speaking_level",
        "overall_assessment",
    ]
    for field in editable_fields:
        edited_profile[field] = st.text_input(field.replace("_", " ").title(), value=profile.get(field, ""))

    cv_drive_link = st.text_input(
        "Google Drive link for CV (required by form)",
        value="",
        placeholder="https://drive.google.com/file/d/.../view",
    )

    st.subheader("Referral options (required form fields)")
    project_referred = st.multiselect("Which projects are you referring to?", PROJECT_OPTIONS)
    shift_schedule = st.selectbox("Shift schedule candidate is available for", SHIFT_OPTIONS, index=0)
    onboard_timeline = st.selectbox("When can candidate onboard?", ONBOARD_OPTIONS, index=0)

    with st.expander("Show extracted raw CV text"):
        st.text(raw_text[:12000] + ("\n\n[truncated]" if len(raw_text) > 12000 else ""))

    if st.button("Generate Prefilled Link"):
        field_values: dict[str, str | list[str]] = {
            **edited_profile,
            "cv_drive_link": cv_drive_link,
            "project_referred": project_referred,
            "shift_schedule": shift_schedule,
            "onboard_timeline": onboard_timeline,
        }

        field_mapping = {**FORM_FIELD_MAPPING, **FORM_OPTION_ENTRIES}

        prefilled_url = build_prefilled_url(
            base_url=GOOGLE_FORM_BASE_URL,
            field_to_entry=field_mapping,
            field_values=field_values,
        )

        st.success("Prefilled URL generated")
        st.code(prefilled_url, language="text")
        st.markdown(f"[Open prefilled form]({prefilled_url})")

else:
    st.info("Upload a candidate PDF CV to start.")
