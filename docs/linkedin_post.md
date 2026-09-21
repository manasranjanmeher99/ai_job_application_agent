# LinkedIn Post Draft

---

🚀 **I built an AI Job Application Agent — and open-sourced it.**

Job hunting is repetitive: read a JD, guess if you're a fit, rewrite your
resume, write yet another cover letter, then lose track of where you applied.
So I built a tool to automate that whole loop.

**How it works:**
📄 Upload your resume (PDF/TXT)
💼 Paste or pick a job description
📊 Get an instant match score — TF-IDF text similarity blended with a
curated 100+ skill taxonomy (ML, cloud, data eng, BI, soft skills)
🧩 See exactly which required skills you're missing (skill gap analysis)
🔑 Get an ATS keyword report — the literal terms recruiting systems scan for
✉️ Generate a personalized cover letter with Google Gemini (grounded in your
actual resume — no fabricated experience)
📝 Get concrete resume improvement suggestions for that specific job
🎤 Get likely interview topics based on the role and your skill gaps
📌 Save everything to a built-in SQLite application tracker

**Stack:** Python, Streamlit, scikit-learn (TF-IDF + cosine similarity),
Google Gemini API, SQLite, pytest.

**A detail I'm proud of:** every AI feature has a deterministic template
fallback. No API key configured? The app still works end-to-end — it just
swaps live generation for smart templates. That made it trivial to test,
demo, and keep the repo runnable for anyone who clones it.

This project pulled together the full stack I care about — NLP feature
engineering, prompt design, and shipping something that's actually usable,
not just a notebook.

Code + README + tests on GitHub: [link]

#GenerativeAI #DataScience #MachineLearning #Python #NLP #OpenSource
#JobSearch #Streamlit #GoogleGemini #PortfolioProject

---

*Tip: swap in a screenshot or short screen recording of the match-score page
— posts with visuals get noticeably more engagement.*
