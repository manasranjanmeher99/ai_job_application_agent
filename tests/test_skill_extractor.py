from src.skill_extractor import categorize_skills, extract_skills


def test_extract_skills_basic():
    text = "Experienced with Python, SQL, and Machine Learning. Also used AWS and Docker."
    skills = extract_skills(text)
    assert "python" in skills
    assert "sql" in skills
    assert "machine learning" in skills
    assert "aws" in skills
    assert "docker" in skills


def test_extract_skills_symbol_tokens():
    text = "Strong background in C++ and C# development."
    skills = extract_skills(text)
    assert "c++" in skills
    assert "c#" in skills


def test_extract_skills_no_false_positive_substring():
    # "r" should not match inside "for" or "experience"
    text = "I have experience working for a great team."
    skills = extract_skills(text)
    assert "r" not in skills


def test_extract_skills_empty_text():
    assert extract_skills("") == set()
    assert extract_skills(None) == set()


def test_categorize_skills_groups_correctly():
    skills = {"python", "aws", "tableau"}
    grouped = categorize_skills(skills)
    assert "python" in grouped["Programming Languages"]
    assert "aws" in grouped["Cloud & DevOps"]
    assert "tableau" in grouped["Visualization / BI"]
