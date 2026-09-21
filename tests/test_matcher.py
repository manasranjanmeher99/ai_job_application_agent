from src.matcher import compute_match, skill_overlap_score, tfidf_similarity


def test_tfidf_similarity_identical_text_is_high():
    text = "Experienced Python developer with machine learning and SQL skills."
    score = tfidf_similarity(text, text)
    assert score > 90


def test_tfidf_similarity_unrelated_text_is_low():
    resume = "Professional chef specializing in French pastry and baking."
    jd = "Looking for a backend engineer skilled in Java, Kubernetes, and microservices."
    score = tfidf_similarity(resume, jd)
    assert score < 30


def test_tfidf_similarity_empty_inputs():
    assert tfidf_similarity("", "something") == 0.0
    assert tfidf_similarity("something", "") == 0.0


def test_skill_overlap_score_full_match():
    resume_skills = {"python", "sql", "aws"}
    jd_skills = {"python", "sql"}
    assert skill_overlap_score(resume_skills, jd_skills) == 100.0


def test_skill_overlap_score_partial_match():
    resume_skills = {"python"}
    jd_skills = {"python", "sql"}
    assert skill_overlap_score(resume_skills, jd_skills) == 50.0


def test_skill_overlap_score_no_jd_skills():
    assert skill_overlap_score({"python"}, set()) == 100.0


def test_compute_match_returns_expected_keys():
    resume = "Data scientist with Python, SQL, and machine learning experience."
    jd = "Seeking a data scientist with Python, SQL, and machine learning skills."
    result = compute_match(resume, jd)
    expected_keys = {
        "overall_score", "tfidf_score", "skill_score", "resume_skills",
        "jd_skills", "matched_skills", "missing_skills", "extra_skills",
    }
    assert expected_keys.issubset(result.keys())
    assert result["overall_score"] > 50
    assert "python" in result["matched_skills"]
