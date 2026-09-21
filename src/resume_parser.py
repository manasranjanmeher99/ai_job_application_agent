"""Extract plain text from an uploaded resume (.pdf or .txt)."""
from io import BytesIO


class ResumeParseError(Exception):
    pass


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file's raw bytes using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise ResumeParseError(
            "pypdf is not installed. Run: pip install pypdf"
        ) from e

    reader = PdfReader(BytesIO(file_bytes))
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text() or "")
    text = "\n".join(pages_text).strip()

    if not text:
        raise ResumeParseError(
            "No extractable text found in this PDF. It may be a scanned "
            "image — try exporting your resume as a text-based PDF or .txt."
        )
    return text


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode a plain-text resume file."""
    for encoding in ("utf-8", "latin-1"):
        try:
            return file_bytes.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    raise ResumeParseError("Could not decode the .txt file's encoding.")


def parse_resume(filename: str, file_bytes: bytes) -> str:
    """Dispatch to the right extractor based on file extension."""
    name = filename.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    if name.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    raise ResumeParseError(
        f"Unsupported file type for '{filename}'. Please upload a .pdf or .txt resume."
    )
