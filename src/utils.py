"""Small shared text-processing helpers used across the app."""
import re

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "of", "to", "in",
    "on", "for", "with", "as", "by", "at", "from", "is", "are", "was", "were",
    "be", "been", "being", "this", "that", "these", "those", "it", "its",
    "we", "you", "your", "our", "their", "they", "he", "she", "his", "her",
    "will", "would", "can", "could", "should", "may", "might", "must",
    "have", "has", "had", "do", "does", "did", "not", "no", "yes", "about",
    "into", "over", "under", "than", "such", "also", "which", "who", "whom",
    "job", "role", "work", "working", "team", "years", "year", "experience",
    "including", "etc", "us", "using",
}


def clean_text(text: str) -> str:
    """Lowercase, strip punctuation noise, collapse whitespace."""
    if not text:
        return ""
    text = text.replace("\u2019", "'")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str):
    """Very small tokenizer: lowercase word tokens, letters/digits/+/#/. allowed
    (so things like 'c++', 'c#', 'node.js' survive)."""
    text = text.lower()
    tokens = re.findall(r"[a-z0-9][a-z0-9+#.]*", text)
    return [t.strip(".") for t in tokens if t.strip(".") and t not in STOPWORDS]


def top_ngrams_diff(text: str, exclude_words: set, n_top: int = 20):
    """Return the most frequent single words in `text` that are NOT already
    covered by `exclude_words`. Used as a lightweight fallback keyword source
    alongside the curated skill list."""
    from collections import Counter

    tokens = [t for t in tokenize(text) if len(t) > 2 and t not in exclude_words]
    counts = Counter(tokens)
    return [word for word, _ in counts.most_common(n_top)]
