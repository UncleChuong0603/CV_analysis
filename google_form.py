from __future__ import annotations

from typing import Dict
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def parse_prefill_template(prefill_url: str) -> tuple[str, Dict[str, str]]:
    parsed = urlparse(prefill_url)
    query = parse_qs(parsed.query)
    entry_map = {k: v[0] for k, v in query.items() if k.startswith("entry.") and v}
    base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    return base_url, entry_map


def build_prefilled_url(
    base_url: str,
    field_to_entry: Dict[str, str],
    field_values: Dict[str, str | list[str]],
    keep_empty: bool = False,
) -> str:
    params: list[tuple[str, str]] = []

    for field, entry_id in field_to_entry.items():
        value = field_values.get(field)

        if isinstance(value, list):
            for item in value:
                item = (item or "").strip()
                if item or keep_empty:
                    params.append((entry_id, item))
        else:
            str_val = (value or "").strip() if value is not None else ""
            if str_val or keep_empty:
                params.append((entry_id, str_val))

    query = urlencode(params, doseq=True)
    return f"{base_url}?{query}" if query else base_url
