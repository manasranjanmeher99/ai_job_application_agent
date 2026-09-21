import pytest

from src.resume_parser import ResumeParseError, extract_text_from_txt, parse_resume


def test_extract_text_from_txt():
    content = b"Jane Doe\nData Scientist\nPython, SQL, Machine Learning"
    text = extract_text_from_txt(content)
    assert "Jane Doe" in text
    assert "Python" in text


def test_extract_text_from_txt_latin1_fallback():
    content = "Café Résumé".encode("latin-1")
    text = extract_text_from_txt(content)
    assert "sum" in text  # decoded without crashing


def test_parse_resume_unsupported_extension():
    with pytest.raises(ResumeParseError):
        parse_resume("resume.docx", b"irrelevant")


def test_parse_resume_dispatches_txt():
    text = parse_resume("resume.txt", b"Python developer with 5 years experience")
    assert "Python" in text
