import unittest

from cv_parser import extract_candidate_profile
from google_form import build_prefilled_url, parse_prefill_template


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
        self.assertEqual(profile["full_name"], "John Doe")
        self.assertEqual(profile["email"], "john.doe@example.com")
        self.assertIn("555", profile["phone"])
        self.assertIn("linkedin.com", profile["linkedin"])
        self.assertIn("github.com", profile["github"])
        self.assertEqual(profile["years_experience"], "8")


class TestGoogleForm(unittest.TestCase):
    def test_prefill_parser_and_builder(self):
        url = "https://docs.google.com/forms/d/e/abc/viewform?usp=pp_url&entry.1=Foo&entry.2=Bar"
        base, entries = parse_prefill_template(url)
        self.assertTrue(base.endswith("/viewform"))
        self.assertEqual(entries["entry.1"], "Foo")

        prefilled = build_prefilled_url(
            base_url=base,
            field_to_entry={"full_name": "entry.1", "email": "entry.2"},
            field_values={"full_name": "John", "email": "john@example.com"},
        )
        self.assertIn("entry.1=John", prefilled)
        self.assertIn("entry.2=john%40example.com", prefilled)


if __name__ == "__main__":
    unittest.main()
