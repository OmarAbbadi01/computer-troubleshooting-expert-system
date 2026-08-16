"""Rendering helpers for user-facing texts in a selected language.

Every user-facing string in the JSON data files is an object with two
keys: "en" (English) and "ar" (Arabic). The CLI asks the user to pick a
language once, at the start, and then renders every text in that language
only. These helpers contain no domain logic at all.
"""

from __future__ import annotations

from typing import Dict


def render(text: Dict[str, str], lang: str = "en") -> str:
    """Return the text in the selected language (falls back to English)."""
    return text.get(lang) or text.get("en", "")

