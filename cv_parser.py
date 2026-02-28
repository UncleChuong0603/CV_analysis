from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List



@dataclass
class CandidateProfile:
    full_name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    current_title: str = ""
    current_company: str = ""
    years_experience: str = ""
    education_highest: str = ""
    skills: str = ""

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
    for ln in lines[:8]:
        if re.search(r"@|linkedin|github|curriculum|resume|cv|phone|email", ln, re.IGNORECASE):
            continue
        if 2 <= len(ln.split()) <= 4 and ln.replace(" ", "").replace("-", "").isalpha():
            return ln
    return ""


def _guess_current_title_and_company(text: str) -> tuple[str, str]:
    patterns = [
        r"(?:Experience|Work Experience|Employment)[:\s\n]+([^\n]{3,120})",
        r"(?m)^([A-Z][^\n]{2,80})\s+at\s+([A-Z][^\n]{1,80})$",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            segment = m.group(1)
            if " at " in segment.lower():
                parts = re.split(r"\s+at\s+", segment, flags=re.IGNORECASE)
                if len(parts) >= 2:
                    return _normalize_spaces(parts[0]), _normalize_spaces(parts[1])
    m2 = re.search(r"(?m)^([A-Z][A-Za-z0-9 /&,-]{2,60})\s+at\s+([A-Z][A-Za-z0-9 /&,-]{2,60})$", text)
    if m2:
        return _normalize_spaces(m2.group(1)), _normalize_spaces(m2.group(2))
    return "", ""


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
    priority = [
        r"Ph\.?D",
        r"Doctor(?:ate)?",
        r"Master(?:'s)?",
        r"M\.Sc",
        r"MBA",
        r"Bachelor(?:'s)?",
        r"B\.Sc",
        r"B\.Eng",
        r"Diploma",
    ]
    for degree in priority:
        m = re.search(degree, text, re.IGNORECASE)
        if m:
            return m.group(0)
    return ""


def _guess_skills(text: str, top_n: int = 10) -> str:
    text_lower = text.lower()
    known_skills = [
        "python", "java", "javascript", "typescript", "sql", "aws", "gcp", "azure",
        "docker", "kubernetes", "react", "node", "flask", "django", "fastapi",
        "pandas", "numpy", "machine learning", "data analysis", "excel", "tableau",
        "power bi", "git", "linux", "terraform",
    ]

    found = []
    for s in known_skills:
        count = text_lower.count(s)
        if count > 0:
            found.extend([s] * count)

    if not found:
        return ""

    counts = Counter(found)
    top = [k for k, _ in counts.most_common(top_n)]
    return ", ".join(top)


def extract_candidate_profile(cv_text: str) -> CandidateProfile:
    title, company = _guess_current_title_and_company(cv_text)
    return CandidateProfile(
        full_name=_guess_name(cv_text),
        email=_find_email(cv_text),
        phone=_find_phone(cv_text),
        linkedin=_find_url(cv_text, "linkedin.com"),
        github=_find_url(cv_text, "github.com"),
        current_title=title,
        current_company=company,
        years_experience=_guess_years_experience(cv_text),
        education_highest=_guess_education(cv_text),
        skills=_guess_skills(cv_text),
    )
