# 🧠 AI Job Application Agent

An end-to-end **Generative AI + Data Science** app that helps job seekers tailor
every application. Upload a resume, pick (or paste) a job description, and get
an instant match score, a skill-gap breakdown, ATS keyword recommendations,
and AI-generated cover letters / resume tips / interview prep — then track
every application in one place.

**Workflow:**

```
Resume → Job Description → AI Match Analysis → Skill Gap → ATS Keywords
       → Tailored Application (Cover Letter / Resume Tips / Interview Prep)
       → Application Tracker
```

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)


---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Resume Parser | Extracts text from `.pdf` or `.txt` resumes |
| 📊 Match Scoring | TF-IDF + cosine similarity blended with curated skill overlap |
| 🧩 Skill Gap Analysis | Shows matched, missing, and extra skills vs. the job description |
| 🔑 ATS Keyword Detection | Surfaces literal keywords the JD uses that your resume is missing |
| ✉️ AI Cover Letter | Google Gemini-generated, personalized to your real experience |
| 📝 Resume Suggestions | Concrete, actionable edits tailored to the specific job |
| 🎤 Interview Prep | Likely technical + behavioral topics based on the JD and your gaps |
| 📌 Application Tracker | SQLite-backed tracker with status pipeline (Saved → Applied → Interviewing → Offer) |
| 🌐 Job Dataset | 10 sample job postings included to try the app instantly, no setup required |
| 🧪 Unit Tests | `pytest` suite covering parsing, matching, ATS keywords, and the tracker |
| 🛟 Offline-Safe | Every AI feature has a deterministic template fallback if no API key is set |

---

## 🖥️ Screens

1. **Analyze Match** — upload resume + pick/paste a JD → get score, skill gap, ATS keywords
2. **AI Assistant** — generate cover letter, resume tips, interview prep; save to tracker
3. **Application Tracker** — view, update status, open postings, delete entries

---

## 🏗️ Architecture

```
ai_job_application_agent/
├── app.py                  # Streamlit UI (3-page workflow)
├── src/
│   ├── resume_parser.py    # PDF/TXT text extraction
│   ├── skill_extractor.py  # Curated skills taxonomy + regex matching
│   ├── matcher.py          # TF-IDF cosine similarity + skill overlap scoring
│   ├── ats_keywords.py     # Missing ATS keyword detection
│   ├── gemini_client.py    # Google Gemini API wrapper (graceful fallback)
│   ├── cover_letter.py     # AI cover letter / resume tips / interview prep generation
│   ├── tracker.py          # SQLite application tracker (CRUD)
│   └── utils.py            # Shared text-cleaning helpers
├── data/jobs.csv           # Sample job postings dataset
├── tests/                  # pytest unit tests
├── docs/                   # LinkedIn post + resume bullet copy
├── requirements.txt
└── .env.example
```

**Design principle:** every AI-powered feature (`gemini_client.py`,
`cover_letter.py`) fails soft — if no `GEMINI_API_KEY` is configured, or the
API call errors out, the app falls back to a deterministic template so the
tool is always usable, including for demos and CI.

---

## 🚀 Getting Started

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/ai-job-application-agent.git
cd ai-job-application-agent
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. (Optional) Add your Gemini API key

Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

```bash
cp .env.example .env
# then edit .env and paste your key
```

> The app works fully without a key — the AI Assistant page falls back to
> smart templates instead of live Gemini generation.

### 3. Run the app

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

### 4. Run the tests

```bash
pytest tests/ -v
```

---

## 🧠 How the Match Score Works

The overall score blends two signals:

- **TF-IDF cosine similarity (40%)** — overall topical/semantic overlap
  between the full resume and job description text.
- **Curated skill overlap (60%)** — percentage of the job's required skills
  (from a taxonomy of 100+ programming languages, ML/DS tools, cloud
  platforms, databases, BI tools, and soft skills) that also appear in the
  resume.

This keeps the score honest: generic text similarity alone can be gamed, and
skill-keyword matching alone misses context — combining both gives a more
reliable signal, and the UI shows both components transparently rather than
a single black-box number.

---

## 🛣️ Roadmap Ideas

- [ ] Multi-resume comparison against one JD
- [ ] Browser extension to pull JD text directly from job boards
- [ ] Support for `.docx` resumes
- [ ] Export tracker to CSV / Google Sheets
- [ ] Auto-fill application forms via Playwright

---


## 🙌 Contributing

Issues and PRs welcome! This project was built as a portfolio piece
demonstrating applied GenAI + Data Science skills: NLP feature engineering,
prompt engineering, resilient AI-integration patterns, and a full-stack
Streamlit application.
