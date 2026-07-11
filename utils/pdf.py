"""Shared ReportLab helpers - Unicode/Arabic font registration and safe text
encoding. Originally lived only in blueprints/reports/routes.py; extracted
here so services/contracts.py can reuse the same PDF stack instead of
introducing a second one.
"""
import os
import re

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    import arabic_reshaper
except Exception:  # pragma: no cover - optional runtime dependency
    arabic_reshaper = None

try:
    from bidi.algorithm import get_display
except Exception:  # pragma: no cover - optional runtime dependency
    get_display = None


_ARABIC_RE = re.compile(r"[\u0600-\u06FF]")


def register_unicode_font():
    """Try to register a Unicode-capable font for ReportLab.

    Returns the font name if registered, else None.
    """
    candidates = [
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/ttf/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/google-noto/NotoSans-Regular.ttf",
    ]

    for path in candidates:
        if os.path.isfile(path):
            try:
                font_name = "UnicodeSans"
                if font_name not in pdfmetrics.getRegisteredFontNames():
                    pdfmetrics.registerFont(TTFont(font_name, path))
                return font_name
            except Exception:
                continue

    return None


def safe_pdf_text(value, allow_unicode: bool):
    if value is None:
        return ""
    text = str(value)
    if allow_unicode:
        return text
    return text.encode("latin-1", "replace").decode("latin-1")


def safe_rtl_pdf_text(value, allow_unicode: bool):
    text = safe_pdf_text(value, allow_unicode)
    if not allow_unicode or not text or not _ARABIC_RE.search(text):
        return text
    if arabic_reshaper and get_display:
        try:
            return get_display(arabic_reshaper.reshape(text))
        except Exception:
            return text
    return text
