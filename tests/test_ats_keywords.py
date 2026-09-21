from src.ats_keywords import extract_top_jd_terms, find_missing_ats_keywords


def test_extract_top_jd_terms_nonempty():
    jd = "We need a data scientist skilled in Python, SQL, and machine learning."
    terms = extract_top_jd_terms(jd, top_n=10)
    assert len(terms) > 0


def test_find_missing_ats_keywords_detects_gap():
    resume = "Marketing specialist with strong writing and social media skills."
    jd = "Looking for a data scientist with Python, SQL, and machine learning experience."
    result = find_missing_ats_keywords(resume, jd)
    assert "python" in result["missing_skill_keywords"]
    assert "sql" in result["missing_skill_keywords"]


def test_find_missing_ats_keywords_no_gap_when_covered():
    resume = "Data scientist skilled in Python, SQL, and machine learning."
    jd = "Looking for a data scientist with Python, SQL, and machine learning experience."
    result = find_missing_ats_keywords(resume, jd)
    assert "python" not in result["missing_skill_keywords"]
    assert "sql" not in result["missing_skill_keywords"]
