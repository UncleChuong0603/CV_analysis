from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class CandidateProfile:
    candidate_full_name: str = ""
    candidate_email: str = ""
    candidate_phone: str = ""
    linkedin: str = ""
    github: str = ""
    position_referred: str = ""
    candidate_team: str = ""
    years_experience: str = ""
    education_highest: str = ""
    skills: str = ""
    english_speaking_level: str = ""
    overall_assessment: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {k: (v or "") for k, v in asdict(self).items()}


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    text_parts: List[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text)
    return "\n".join(text_parts)


def _normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _find_email(text: str) -> str:
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return m.group(0) if m else ""


def _find_phone(text: str) -> str:
    m = re.search(r"(?:\+?\d[\d\s().-]{8,}\d)", text)
    return _normalize_spaces(m.group(0)) if m else ""


def _find_url(text: str, domain_keyword: str) -> str:
    pattern = rf"(?:https?://)?(?:www\.)?{re.escape(domain_keyword)}/[^\s|,;)]*"
    m = re.search(pattern, text, flags=re.IGNORECASE)
    if not m:
        return ""
    url = m.group(0)
    if not url.lower().startswith("http"):
        url = f"https://{url}"
    return url


def _guess_name(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines[:10]:
        if re.search(r"@|linkedin|github|curriculum|resume|cv|phone|email", ln, re.IGNORECASE):
            continue
        cleaned = ln.replace(" ", "").replace("-", "")
        if 2 <= len(ln.split()) <= 5 and cleaned.isalpha():
            return ln
    return ""


def _guess_position(text: str) -> str:
    m = re.search(r"(?im)^(senior|junior|lead|principal)?\s*[a-z][^\n]{0,50}(engineer|developer|analyst|manager|consultant)[^\n]*$", text)
    if m:
        return _normalize_spaces(m.group(0))

    m2 = re.search(r"(?m)^([A-Z][A-Za-z0-9 /&,-]{2,70})\s+at\s+([A-Z][A-Za-z0-9 /&,-]{2,60})$", text)
    if m2:
        return _normalize_spaces(m2.group(1))
    return ""


def _guess_years_experience(text: str) -> str:
    m = re.search(r"(\d{1,2})\+?\s*(?:years|yrs)\s+(?:of\s+)?experience", text, re.IGNORECASE)
    if m:
        return m.group(1)

    years = [int(y) for y in re.findall(r"\b(19\d{2}|20\d{2})\b", text)]
    if len(years) >= 2:
        span = max(years) - min(years)
        if 0 < span <= 45:
            return str(span)
    return ""


def _guess_education(text: str) -> str:
    priority = [r"Ph\.?D", r"Doctor(?:ate)?", r"Master(?:'s)?", r"M\.Sc", r"MBA", r"Bachelor(?:'s)?", r"B\.Sc", r"B\.Eng", r"Diploma"]
    for degree in priority:
        m = re.search(degree, text, re.IGNORECASE)
        if m:
            return m.group(0)
    return ""


def _guess_skills(text: str, top_n: int = 8) -> str:
    text_lower = text.lower()
    known_skills = [
        "python", "java", "javascript", "typescript", "sql", "aws", "gcp", "azure", "docker", "kubernetes", "react", "node", "flask", "django", "fastapi", "pandas", "numpy", "machine learning", "data analysis", "excel", "tableau", "power bi", "git", "linux", "terraform",
    ]
    found = []
    for skill in known_skills:
        count = text_lower.count(skill)
        if count > 0:
            found.extend([skill] * count)
    if not found:
        return ""
    counts = Counter(found)
    return ", ".join([k for k, _ in counts.most_common(top_n)])


def _guess_english_level(text: str) -> str:
    m = re.search(r"(IELTS\s*\d(?:\.\d)?)|(TOEIC\s*\d+)|(English\s*:\s*[^\n]{1,40})", text, re.IGNORECASE)
    return _normalize_spaces(m.group(0)) if m else ""


def _build_overall_assessment(position: str, years_experience: str, skills: str) -> str:
    parts = []
    if position:
        parts.append(f"Candidate aligns with role: {position}.")
    if years_experience:
        parts.append(f"Estimated {years_experience} years of experience.")
    if skills:
        parts.append(f"Key skills: {skills}.")
    return " ".join(parts)


def extract_candidate_profile(cv_text: str) -> CandidateProfile:
    position = _guess_position(cv_text)
    years_experience = _guess_years_experience(cv_text)
    skills = _guess_skills(cv_text)

    return CandidateProfile(
        candidate_full_name=_guess_name(cv_text),
        candidate_email=_find_email(cv_text),
        candidate_phone=_find_phone(cv_text),
        linkedin=_find_url(cv_text, "linkedin.com"),
        github=_find_url(cv_text, "github.com"),
        position_referred=position,
        candidate_team="",
        years_experience=years_experience,
        education_highest=_guess_education(cv_text),
        skills=skills,
        english_speaking_level=_guess_english_level(cv_text),
        overall_assessment=_build_overall_assessment(position, years_experience, skills),
    )
