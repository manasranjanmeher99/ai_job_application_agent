"""AI-assisted application content: cover letters, resume improvement
suggestions, and likely interview topics.

Every generator tries Gemini first (richer, personalized output) and falls
back to a deterministic template if no API key is configured or the call
fails — so the app is always usable, even fully offline.
"""
from . import gemini_client


def generate_cover_letter(
    resume_text: str,
    jd_text: str,
    company: str,
    role: str,
    matched_skills: list,
    missing_skills: list,
    candidate_name: str = "",
) -> str:
    prompt = f"""You are an expert career coach. Write a concise, specific,
professional cover letter (3-4 short paragraphs, under 300 words) for the
role of "{role}" at "{company}".

Candidate name: {candidate_name or "[Your Name]"}

Use the candidate's actual background from their resume below — reference
real skills/experience, don't invent facts. Naturally weave in these
matched skills where truthful: {", ".join(matched_skills) or "N/A"}.
Do not claim skills the candidate doesn't have. Keep tone confident but not
arrogant, and end with a clear call to action.

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{jd_text[:3000]}
"""
    ai_text = gemini_client.generate_text(prompt)
    if ai_text:
        return ai_text

    # --- Deterministic fallback template ---
    name = candidate_name or "[Your Name]"
    skills_line = ", ".join(matched_skills[:6]) if matched_skills else "a strong technical foundation"
    return f"""Dear Hiring Manager,

I am excited to apply for the {role} position at {company}. Reviewing the
job description, I was struck by how closely it aligns with my background,
particularly in {skills_line}.

In my recent experience, I have applied these skills to deliver measurable
results, and I am confident I can bring the same focus and rigor to your
team. I am especially drawn to this role because it offers the opportunity
to contribute to meaningful, high-impact work at {company}.

I would welcome the chance to discuss how my experience can support your
team's goals. Thank you for your time and consideration.

Sincerely,
{name}

[Note: This is a template fallback. Add a GEMINI_API_KEY in your .env file
for a fully personalized, AI-generated cover letter.]"""


def generate_resume_suggestions(
    resume_text: str, jd_text: str, missing_skills: list
) -> str:
    prompt = f"""You are a resume coach. Compare the resume and job
description below. Give 5-7 short, specific, actionable bullet-point
suggestions to improve the resume for THIS job — e.g. keywords to add
(only if truthfully applicable), quantifying achievements, reordering
sections, or rephrasing bullets. Do not suggest fabricating experience.

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{jd_text[:3000]}

MISSING SKILLS DETECTED (mention only if genuinely relevant): {", ".join(missing_skills) or "None"}
"""
    ai_text = gemini_client.generate_text(prompt)
    if ai_text:
        return ai_text

    bullets = [
        "Quantify your achievements with numbers (%, $, time saved, users impacted).",
        "Mirror the exact phrasing the job description uses for key skills (helps ATS matching).",
        "Move your most relevant experience/projects to the top of each section.",
        "Trim outdated or irrelevant experience to keep the resume focused and skimmable.",
        "Use strong action verbs (built, led, optimized, automated) instead of passive phrasing.",
    ]
    if missing_skills:
        bullets.append(
            "If you genuinely have experience with any of these, add them explicitly: "
            + ", ".join(missing_skills[:8])
        )
    bullets.append(
        "[Note: This is a template fallback. Add a GEMINI_API_KEY in your .env "
        "file for personalized, AI-generated suggestions.]"
    )
    return "\n".join(f"- {b}" for b in bullets)


def generate_interview_topics(
    jd_text: str, missing_skills: list, matched_skills: list
) -> str:
    prompt = f"""You are a technical interview coach. Based on this job
description, list 6-8 likely interview topics/questions the candidate
should prepare for, grouped as (1) technical/skill-based and (2)
behavioral. Prioritize topics tied to these required skills:
{", ".join(matched_skills + missing_skills) or "general role requirements"}.

JOB DESCRIPTION:
{jd_text[:3000]}
"""
    ai_text = gemini_client.generate_text(prompt)
    if ai_text:
        return ai_text

    lines = ["Technical:"]
    for skill in (matched_skills + missing_skills)[:6] or ["core responsibilities"]:
        lines.append(f"- Be ready to discuss your hands-on experience with {skill}.")
    lines.append("\nBehavioral:")
    lines.extend(
        [
            "- Describe a time you handled a tight deadline or ambiguous requirements.",
            "- Tell me about a project you're most proud of and why.",
            "- Describe a disagreement with a teammate and how you resolved it.",
        ]
    )
    lines.append(
        "\n[Note: This is a template fallback. Add a GEMINI_API_KEY in your "
        ".env file for tailored, AI-generated interview prep.]"
    )
    return "\n".join(lines)
