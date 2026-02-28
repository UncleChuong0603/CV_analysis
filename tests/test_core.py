import unittest

from cv_parser import extract_candidate_profile
from form_config import FORM_FIELD_MAPPING, GOOGLE_FORM_BASE_URL
from google_form import build_prefilled_url


class TestCVParser(unittest.TestCase):
    def test_extract_candidate_profile(self):
        text = """
John Doe
Email: john.doe@example.com
Phone: +1 (555) 123-4567
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe
Senior Software Engineer at Acme Corp
8 years of experience
Education: Master's in Computer Science
Skills: Python, SQL, AWS, Docker, React
"""
        profile = extract_candidate_profile(text).to_dict()
        self.assertEqual(profile["candidate_full_name"], "John Doe")
        self.assertEqual(profile["candidate_email"], "john.doe@example.com")
        self.assertIn("555", profile["candidate_phone"])
        self.assertEqual(profile["years_experience"], "8")
        self.assertIn("skills", profile)


class TestGoogleForm(unittest.TestCase):
    def test_prefill_builder_supports_multiselect(self):
        prefilled = build_prefilled_url(
            base_url=GOOGLE_FORM_BASE_URL,
            field_to_entry={
                "candidate_full_name": FORM_FIELD_MAPPING["candidate_full_name"],
                "project_referred": "entry.1457734049",
            },
            field_values={
                "candidate_full_name": "John Doe",
                "project_referred": ["Azure", "O365"],
            },
        )
        self.assertIn("entry.1048297419=John+Doe", prefilled)
        self.assertIn("entry.1457734049=Azure", prefilled)
        self.assertIn("entry.1457734049=O365", prefilled)


if __name__ == "__main__":
    unittest.main()
