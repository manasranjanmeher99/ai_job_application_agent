"""Thin wrapper around Google's Gemini API.

Designed so the rest of the app never has to care whether an API key is
configured: `generate_text` returns `None` on any failure (missing key,
missing package, network/quota error) and callers fall back to template
based generation. This keeps the app fully usable in demo/offline mode.
"""
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
_API_KEY = os.getenv("GEMINI_API_KEY")

_model = None
_init_error = None

if _API_KEY:
    try:
        import google.generativeai as genai

        genai.configure(api_key=_API_KEY)
        _model = genai.GenerativeModel(_MODEL_NAME)
    except Exception as e:  # pragma: no cover - environment dependent
        _init_error = str(e)
        _model = None


def is_configured() -> bool:
    """Whether a usable Gemini model is available."""
    return _model is not None


def get_init_error() -> str:
    return _init_error or "GEMINI_API_KEY not set."


def generate_text(prompt: str, max_output_tokens: int = 1024) -> Optional[str]:
    """Call Gemini with `prompt`. Returns the text, or None on any failure."""
    if _model is None:
        return None
    try:
        response = _model.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_output_tokens, "temperature": 0.7},
        )
        return (response.text or "").strip() or None
    except Exception:
        return None
