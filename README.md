# CV PDF → Company Google Form Prefill Tool

This app is tailored to your Google Form:

`https://docs.google.com/forms/d/e/1FAIpQLSfj7dsIMMWBUCSxss7KLGN-dPaANW5awtX44Er0lFmr3VorBg/viewform`

## What it does

1. Upload a candidate CV in PDF.
2. Extract candidate data from CV text.
3. Let you review/edit extracted values.
4. Generate a prefilled Google Form URL for candidate-related fields.

## Auto-filled form fields

- Candidate full name
- Position referred
- Candidate team
- Candidate email
- Candidate phone number
- English speaking level
- Overall assessment
- CV Google Drive link (provided manually in app)
- Projects referred (multi-select in app)
- Shift schedule (select in app)
- Onboard timeline (select in app)

## Not auto-filled

Your personal referral fields (your Vietnamese/English name, iTechwx code, your project/team) are intentionally not populated from CV and can be completed manually in the form.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Parsing is heuristic-based; always review before opening the final prefilled form.
- For scanned image PDFs, integrate OCR in a next step.
