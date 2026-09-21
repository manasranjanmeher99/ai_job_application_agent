"""Curated skills taxonomy + extraction of skills mentioned in free text.

The taxonomy is intentionally broad (data science / ML / software / cloud /
soft skills) so the tool is useful beyond a single job family. Matching is
done with word-boundary regex on a cleaned/lowered version of the text so
multi-word skills ("machine learning") and symbol-bearing ones ("c++", "c#")
are both handled correctly.
"""
import re

SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "sql",
        "r", "go", "golang", "scala", "rust", "matlab", "bash", "shell",
        "php", "ruby", "kotlin", "swift",
    ],
    "Data Science / ML": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "generative ai", "genai", "llm", "large language model",
        "transformers", "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn",
        "pandas", "numpy", "opencv", "xgboost", "lightgbm", "hugging face",
        "langchain", "llamaindex", "rag", "prompt engineering", "fine-tuning",
        "reinforcement learning", "statistics", "a/b testing", "time series",
        "feature engineering", "data mining", "predictive modeling",
    ],
    "Data Engineering / Big Data": [
        "spark", "pyspark", "hadoop", "kafka", "airflow", "etl", "data pipeline",
        "data warehouse", "snowflake", "redshift", "bigquery", "databricks",
        "dbt",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "ci/cd",
        "jenkins", "terraform", "linux", "git", "github", "gitlab", "mlops",
        "sagemaker", "vertex ai",
    ],
    "Databases": [
        "mysql", "postgresql", "postgres", "mongodb", "nosql", "elasticsearch",
        "redis", "cassandra", "dynamodb",
    ],
    "Visualization / BI": [
        "tableau", "power bi", "matplotlib", "seaborn", "plotly", "excel",
        "looker",
    ],
    "Web / App Dev": [
        "streamlit", "flask", "django", "fastapi", "react", "node.js",
        "rest api", "graphql",
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "stakeholder management", "project management", "collaboration",
        "presentation", "mentoring", "agile", "scrum",
    ],
}

ALL_SKILLS = sorted(
    {skill for group in SKILL_TAXONOMY.values() for skill in group},
    key=len,
    reverse=True,  # match longer/multi-word phrases before their substrings
)


def _skill_pattern(skill: str) -> re.Pattern:
    """Build a safe, boundary-aware regex for a skill phrase."""
    escaped = re.escape(skill)
    # allow the escaped phrase but keep word boundaries meaningful even for
    # tokens containing symbols like c++ or c#
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", re.IGNORECASE)


_PATTERNS = {skill: _skill_pattern(skill) for skill in ALL_SKILLS}


def extract_skills(text: str) -> set:
    """Return the set of taxonomy skills found in `text`."""
    if not text:
        return set()
    lowered = text.lower()
    found = set()
    for skill, pattern in _PATTERNS.items():
        if pattern.search(lowered):
            found.add(skill)
    return found


def categorize_skills(skills: set) -> dict:
    """Group a flat set of skills back into taxonomy categories."""
    result = {category: [] for category in SKILL_TAXONOMY}
    for skill in skills:
        for category, members in SKILL_TAXONOMY.items():
            if skill in members:
                result[category].append(skill)
                break
    return {k: sorted(v) for k, v in result.items() if v}
