"""AI Job Application Agent — Streamlit app.

Workflow:
Resume -> Job Description -> AI Match Analysis -> Skill Gap -> ATS Keywords
-> Tailored Application (Cover Letter / Resume Tips / Interview Prep)
-> Application Tracker
"""
import webbrowser

import pandas as pd
import streamlit as st

from src import gemini_client, tracker
from src.ats_keywords import find_missing_ats_keywords
from src.cover_letter import (
    generate_cover_letter,
    generate_interview_topics,
    generate_resume_suggestions,
)
from src.matcher import compute_match
from src.resume_parser import ResumeParseError, parse_resume

st.set_page_config(page_title="AI Job Application Agent", page_icon="🧠", layout="wide")
tracker.init_db()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
for key, default in {
    "resume_text": "",
    "jd_text": "",
    "company": "",
    "role": "",
    "job_url": "",
    "match_result": None,
    "ats_result": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("🧠 AI Job Application Agent")
page = st.sidebar.radio(
    "Navigate",
    ["1. Analyze Match", "2. AI Assistant", "3. Application Tracker"],
)

if gemini_client.is_configured():
    st.sidebar.success("Gemini API connected — AI generation enabled.")
else:
    st.sidebar.warning(
        "No GEMINI_API_KEY found. AI Assistant will use template fallbacks. "
        "Add a key to your .env file to enable full AI generation."
    )

st.sidebar.markdown("---")
st.sidebar.caption(
    "Workflow: Resume → JD → Match Analysis → Skill Gap → ATS Keywords → "
    "Tailored Application → Tracker"
)


# ---------------------------------------------------------------------------
# Page 1: Analyze Match
# ---------------------------------------------------------------------------
if page == "1. Analyze Match":
    st.title("Step 1: Resume ↔ Job Match Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Your Resume")
        uploaded_file = st.file_uploader("Upload resume (.pdf or .txt)", type=["pdf", "txt"])
        if uploaded_file is not None:
            try:
                st.session_state.resume_text = parse_resume(
                    uploaded_file.name, uploaded_file.getvalue()
                )
                st.success(f"Parsed {len(st.session_state.resume_text)} characters from resume.")
            except ResumeParseError as e:
                st.error(str(e))

        st.session_state.resume_text = st.text_area(
            "Or paste/edit resume text directly",
            value=st.session_state.resume_text,
            height=250,
        )

    with col2:
        st.subheader("💼 Job Description")

        try:
            jobs_df = pd.read_csv("data/jobs.csv")
        except FileNotFoundError:
            jobs_df = pd.DataFrame()

        if not jobs_df.empty:
            job_choice = st.selectbox(
                "Pick a sample job (or choose 'Custom' to paste your own)",
                ["Custom"] + [f"{r.company} — {r.role}" for r in jobs_df.itertuples()],
            )
            if job_choice != "Custom":
                idx = [f"{r.company} — {r.role}" for r in jobs_df.itertuples()].index(job_choice)
                row = jobs_df.iloc[idx]
                st.session_state.jd_text = row["description"]
                st.session_state.company = row["company"]
                st.session_state.role = row["role"]
                st.session_state.job_url = row["url"]

        st.session_state.company = st.text_input("Company", value=st.session_state.company)
        st.session_state.role = st.text_input("Role / Job Title", value=st.session_state.role)
        st.session_state.job_url = st.text_input("Job posting URL (optional)", value=st.session_state.job_url)
        st.session_state.jd_text = st.text_area(
            "Job description", value=st.session_state.jd_text, height=170
        )

    st.markdown("---")
    if st.button("🔍 Analyze Match", type="primary", use_container_width=True):
        if not st.session_state.resume_text.strip() or not st.session_state.jd_text.strip():
            st.error("Please provide both a resume and a job description.")
        else:
            with st.spinner("Analyzing..."):
                st.session_state.match_result = compute_match(
                    st.session_state.resume_text, st.session_state.jd_text
                )
                st.session_state.ats_result = find_missing_ats_keywords(
                    st.session_state.resume_text, st.session_state.jd_text
                )

    if st.session_state.match_result:
        result = st.session_state.match_result
        ats = st.session_state.ats_result

        st.markdown("## 📊 Match Analysis")
        m1, m2, m3 = st.columns(3)
        m1.metric("Overall Match Score", f"{result['overall_score']}%")
        m2.metric("Text Similarity (TF-IDF)", f"{result['tfidf_score']}%")
        m3.metric("Skill Coverage", f"{result['skill_score']}%")

        st.progress(min(int(result["overall_score"]), 100))

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("### ✅ Matched Skills")
            st.write(", ".join(result["matched_skills"]) or "_None found_")
        with c2:
            st.markdown("### ⚠️ Missing Skills (Skill Gap)")
            st.write(", ".join(result["missing_skills"]) or "_None — great coverage!_")
        with c3:
            st.markdown("### ➕ Extra Skills on Resume")
            st.write(", ".join(result["extra_skills"]) or "_None_")

        st.markdown("## 🔑 ATS Keyword Check")
        st.caption(
            "Applicant Tracking Systems mostly match literal keywords. "
            "These JD terms are important and currently missing from your resume."
        )
        k1, k2 = st.columns(2)
        with k1:
            st.markdown("**Missing skill keywords**")
            st.write(", ".join(ats["missing_skill_keywords"]) or "_None_")
        with k2:
            st.markdown("**Other missing high-signal JD terms**")
            st.write(", ".join(ats["missing_generic_terms"]) or "_None_")

        st.info("Head to **2. AI Assistant** to generate a tailored cover letter, resume tips, and interview prep.")


# ---------------------------------------------------------------------------
# Page 2: AI Assistant
# ---------------------------------------------------------------------------
elif page == "2. AI Assistant":
    st.title("Step 2: AI-Generated Application Content")

    if not st.session_state.match_result:
        st.warning("Run a match analysis on the **1. Analyze Match** page first.")
    else:
        result = st.session_state.match_result
        candidate_name = st.text_input("Your name (used in the cover letter)", "")

        tab1, tab2, tab3 = st.tabs(["✉️ Cover Letter", "📝 Resume Suggestions", "🎤 Interview Prep"])

        with tab1:
            if st.button("Generate Cover Letter", key="gen_cover"):
                with st.spinner("Writing your cover letter..."):
                    letter = generate_cover_letter(
                        st.session_state.resume_text,
                        st.session_state.jd_text,
                        st.session_state.company or "the company",
                        st.session_state.role or "this role",
                        result["matched_skills"],
                        result["missing_skills"],
                        candidate_name,
                    )
                    st.session_state["cover_letter_text"] = letter
            if st.session_state.get("cover_letter_text"):
                st.text_area("Cover Letter", st.session_state["cover_letter_text"], height=350)
                st.download_button(
                    "⬇️ Download Cover Letter (.txt)",
                    st.session_state["cover_letter_text"],
                    file_name=f"cover_letter_{st.session_state.company or 'draft'}.txt",
                )

        with tab2:
            if st.button("Generate Resume Suggestions", key="gen_resume"):
                with st.spinner("Reviewing your resume..."):
                    suggestions = generate_resume_suggestions(
                        st.session_state.resume_text,
                        st.session_state.jd_text,
                        result["missing_skills"],
                    )
                    st.session_state["resume_suggestions_text"] = suggestions
            if st.session_state.get("resume_suggestions_text"):
                st.markdown(st.session_state["resume_suggestions_text"])

        with tab3:
            if st.button("Generate Interview Prep", key="gen_interview"):
                with st.spinner("Preparing likely interview topics..."):
                    topics = generate_interview_topics(
                        st.session_state.jd_text,
                        result["missing_skills"],
                        result["matched_skills"],
                    )
                    st.session_state["interview_topics_text"] = topics
            if st.session_state.get("interview_topics_text"):
                st.markdown(st.session_state["interview_topics_text"])

        st.markdown("---")
        st.subheader("📌 Save this application to your tracker")
        with st.form("save_application_form"):
            f_company = st.text_input("Company", value=st.session_state.company)
            f_role = st.text_input("Role", value=st.session_state.role)
            f_url = st.text_input("Job URL", value=st.session_state.job_url)
            f_status = st.selectbox("Status", tracker.STATUSES, index=0)
            f_notes = st.text_area("Notes", "")
            submitted = st.form_submit_button("💾 Save to Tracker")
            if submitted:
                tracker.add_application(
                    company=f_company,
                    role=f_role,
                    job_url=f_url,
                    match_score=result["overall_score"],
                    status=f_status,
                    notes=f_notes,
                )
                st.success(f"Saved {f_role} at {f_company} to your tracker!")


# ---------------------------------------------------------------------------
# Page 3: Application Tracker
# ---------------------------------------------------------------------------
elif page == "3. Application Tracker":
    st.title("Step 3: Application Tracker")

    apps = tracker.get_applications()
    if not apps:
        st.info("No applications saved yet. Save one from the **2. AI Assistant** page.")
    else:
        for app in apps:
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                c1.markdown(f"**{app['role']}** at **{app['company']}**")
                c1.caption(app["notes"] or "")
                c2.write(f"Match: {app['match_score']}%" if app["match_score"] is not None else "Match: —")
                c2.caption(f"Added: {app['date_added']}")

                new_status = c3.selectbox(
                    "Status",
                    tracker.STATUSES,
                    index=tracker.STATUSES.index(app["status"]) if app["status"] in tracker.STATUSES else 0,
                    key=f"status_{app['id']}",
                    label_visibility="collapsed",
                )
                if new_status != app["status"]:
                    tracker.update_status(app["id"], new_status)
                    st.rerun()

                with c4:
                    if app["job_url"]:
                        if st.button("🔗 Open Posting", key=f"open_{app['id']}"):
                            try:
                                webbrowser.open(app["job_url"])
                                st.toast("Opening in browser (works when run locally).")
                            except Exception:
                                pass
                        st.markdown(f"[Open link]({app['job_url']})")
                    if st.button("🗑️ Delete", key=f"delete_{app['id']}"):
                        tracker.delete_application(app["id"])
                        st.rerun()

        st.markdown("---")
        st.subheader("📈 Summary")
        df = pd.DataFrame(apps)
        st.bar_chart(df["status"].value_counts())
