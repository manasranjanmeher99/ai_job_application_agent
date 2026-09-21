"""ATS (Applicant Tracking System) keyword detection.

Real ATS platforms mostly do keyword/phrase matching, not semantic
understanding — so surfacing which important JD terms are literally absent
from the resume is one of the highest-value, most concrete pieces of advice
this tool can give.
"""
from sklearn.feature_extraction.text import TfidfVectorizer

from .skill_extractor import extract_skills
from .utils import clean_text, tokenize


def extract_top_jd_terms(jd_text: str, top_n: int = 25):
    """Top TF-IDF-weighted unigrams/bigrams from the JD (single document,
    so this approximates 'terms that appear often and specifically')."""
    jd_clean = clean_text(jd_text)
    if not jd_clean:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 2), max_features=200
    )
    try:
        matrix = vectorizer.fit_transform([jd_clean])
    except ValueError:
        return []

    scores = matrix.toarray()[0]
    terms = vectorizer.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return [term for term, score in ranked[:top_n] if score > 0]


def find_missing_ats_keywords(resume_text: str, jd_text: str, top_n: int = 25) -> dict:
    """Combine curated-skill gaps with generic top-JD-term gaps into one
    ATS keyword report."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    missing_skill_keywords = sorted(jd_skills - resume_skills)

    resume_tokens = set(tokenize(resume_text))
    top_terms = extract_top_jd_terms(jd_text, top_n=top_n)

    missing_generic_terms = []
    for term in top_terms:
        term_tokens = term.split()
        # consider a bigram "present" only if all its words are in resume
        if all(tok in resume_tokens for tok in term_tokens):
            continue
        if term in missing_skill_keywords:
            continue
        missing_generic_terms.append(term)

    return {
        "missing_skill_keywords": missing_skill_keywords,
        "missing_generic_terms": missing_generic_terms[:top_n],
        "top_jd_terms": top_terms,
    }
