# CV PDF → Google Form Prefill Tool

A lightweight self-hosted app that helps recruiters:

1. Upload a candidate CV in PDF format.
2. Extract important candidate info automatically.
3. Generate a Google Form prefilled URL using your company form's `entry.xxxxx` IDs.

## Features

- PDF text extraction (`pypdf`)
- Heuristic candidate field extraction:
  - full name
  - email
  - phone
  - LinkedIn
  - GitHub
  - current title/company
  - years of experience
  - highest education
  - skills
- Editable extracted values before generating link
- Google Form prefilled URL generation

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown by Streamlit (usually `http://localhost:8501`).

## How to set up Google Form prefill

### Option A (recommended): Paste a prefilled template URL

1. In Google Form, click **Get pre-filled link**.
2. Fill sample values, then copy generated URL.
3. Paste it into the app sidebar.

### Option B: Manual mapping

1. Use your Form base URL:
   - `https://docs.google.com/forms/d/e/<FORM_ID>/viewform`
2. Provide JSON mapping from app fields to form entries:

```json
{
  "full_name": "entry.111111111",
  "email": "entry.222222222",
  "phone": "entry.333333333"
}
```

## Notes

- CV parsing is heuristic-based and may need manual correction.
- For scanned/image PDFs, add OCR (e.g., Tesseract) in a future version.
- Keep candidate data handling compliant with your privacy policy.
