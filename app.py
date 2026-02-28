from __future__ import annotations

import json
import tempfile
from pathlib import Path

import streamlit as st

from cv_parser import extract_candidate_profile, extract_text_from_pdf
from google_form import build_prefilled_url, parse_prefill_template


st.set_page_config(page_title="CV → Google Form Helper", layout="wide")
st.title("CV PDF → Google Form Prefill Tool")
st.caption("Self-host this app locally to parse CVs and generate Google Form prefilled links.")


with st.sidebar:
    st.header("Google Form Setup")
    prefill_template_url = st.text_area(
        "Paste an example prefilled link (recommended)",
        placeholder="https://docs.google.com/forms/d/e/.../viewform?usp=pp_url&entry.123=...",
        height=130,
    )

    st.markdown("Or provide a base URL + JSON mapping")
    base_url_manual = st.text_input(
        "Google Form base URL",
        placeholder="https://docs.google.com/forms/d/e/.../viewform",
    )

    mapping_json = st.text_area(
        "Field mapping JSON (field -> entry id)",
        value=json.dumps(
            {
                "full_name": "entry.111111111",
                "email": "entry.222222222",
                "phone": "entry.333333333",
                "linkedin": "entry.444444444",
                "github": "entry.555555555",
                "current_title": "entry.666666666",
                "current_company": "entry.777777777",
                "years_experience": "entry.888888888",
                "education_highest": "entry.999999999",
                "skills": "entry.1010101010",
            },
            indent=2,
        ),
        height=280,
    )

uploaded_pdf = st.file_uploader("Upload candidate CV (PDF)", type=["pdf"])

if uploaded_pdf:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        temp_pdf_path = Path(tmp.name)

    raw_text = extract_text_from_pdf(temp_pdf_path)
    profile = extract_candidate_profile(raw_text).to_dict()

    st.subheader("Extracted Candidate Information")
    edited_profile = {}

    cols = st.columns(2)
    fields = list(profile.keys())
    for idx, field in enumerate(fields):
        col = cols[idx % 2]
        edited_profile[field] = col.text_input(field.replace("_", " ").title(), value=profile[field])

    st.subheader("Raw Extracted Text")
    with st.expander("Show raw CV text"):
        st.text(raw_text[:10000] + ("\n\n[truncated]" if len(raw_text) > 10000 else ""))

    parsed_mapping = {}
    final_base_url = ""

    if prefill_template_url.strip():
        template_base, template_entries = parse_prefill_template(prefill_template_url.strip())
        final_base_url = template_base
        st.info(
            "Template URL detected. Keep custom mapping JSON so fields map to the correct entry IDs."
        )

    if not final_base_url:
        final_base_url = base_url_manual.strip()

    try:
        parsed_mapping = json.loads(mapping_json)
    except json.JSONDecodeError as exc:
        st.error(f"Invalid JSON mapping: {exc}")

    if st.button("Generate Google Form Prefilled Link"):
        if not final_base_url:
            st.error("Please provide either a prefilled template URL or form base URL.")
        elif not parsed_mapping:
            st.error("Please provide a valid field mapping JSON.")
        else:
            prefilled = build_prefilled_url(
                base_url=final_base_url,
                field_to_entry=parsed_mapping,
                field_values=edited_profile,
            )
            st.success("Prefilled link generated.")
            st.code(prefilled, language="text")
            st.markdown(f"[Open prefilled form]({prefilled})")
else:
    st.info("Upload a PDF CV to start.")
