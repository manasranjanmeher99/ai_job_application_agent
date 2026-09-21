"""Resume <-> Job Description matching.

Two complementary signals are combined:
  1. TF-IDF + cosine similarity over the full text (captures overall
     topical/semantic overlap).
  2. Curated-skill overlap (captures concrete, ATS-relevant hard skills).

The final score blends both so a resume can't game the score with generic
text that happens to be topically similar but has none of the required
skills, nor vice versa.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skill_extractor import extract_skills
from .utils import clean_text


def tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """Cosine similarity between resume and JD, scaled 0-100."""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)
    if not resume_clean or not jd_clean:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
    except ValueError:
        # e.g. only stopwords on both sides
        return 0.0

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(score) * 100, 2)


def skill_overlap_score(resume_skills: set, jd_skills: set) -> float:
    """Percentage of JD-required skills that also appear in the resume."""
    if not jd_skills:
        return 100.0
    matched = resume_skills & jd_skills
    return round(len(matched) / len(jd_skills) * 100, 2)


def compute_match(resume_text: str, jd_text: str, tfidf_weight: float = 0.4) -> dict:
    """Full match report between a resume and a job description.

    Returns a dict with the overall score plus the components that make it
    up, so the UI can show a transparent breakdown rather than a black box
    number.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    tfidf_score = tfidf_similarity(resume_text, jd_text)
    skill_score = skill_overlap_score(resume_skills, jd_skills)

    overall = round(tfidf_weight * tfidf_score + (1 - tfidf_weight) * skill_score, 2)

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)
    extra_skills = sorted(resume_skills - jd_skills)

    return {
        "overall_score": overall,
        "tfidf_score": tfidf_score,
        "skill_score": skill_score,
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
    }
