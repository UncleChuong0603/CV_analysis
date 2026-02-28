from __future__ import annotations

from typing import Dict
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def parse_prefill_template(prefill_url: str) -> tuple[str, Dict[str, str]]:
    """
    Parse a Google Form prefilled URL and return:
    - cleaned base URL (without query)
    - entry mapping from query params (entry.XYZ -> current value)
    """
    parsed = urlparse(prefill_url)
    query = parse_qs(parsed.query)
    entry_map = {k: v[0] for k, v in query.items() if k.startswith("entry.") and v}
    base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    return base_url, entry_map


def build_prefilled_url(
    base_url: str,
    field_to_entry: Dict[str, str],
    field_values: Dict[str, str],
    keep_empty: bool = False,
) -> str:
    """
    Build a Google Form prefilled URL.

    field_to_entry example:
      {
        "full_name": "entry.111111111",
        "email": "entry.222222222"
      }
    """
    params: Dict[str, str] = {}
    for field, entry_id in field_to_entry.items():
        value = (field_values.get(field) or "").strip()
        if value or keep_empty:
            params[entry_id] = value

    query = urlencode(params)
    if query:
        return f"{base_url}?{query}"
    return base_url
