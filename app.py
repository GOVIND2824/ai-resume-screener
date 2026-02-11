import streamlit as st
from groq import Groq
from utils import extract_text_from_pdf
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("🤖 AI Resume Screener & JD Matcher")
st.write("Upload a Job Description and resumes to instantly analyze candidates.")

jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
resume_files = st.file_uploader(
    "Upload Resumes (PDFs)",
    type=["pdf"],
    accept_multiple_files=True
)

analyze = st.button("Analyze Resumes")

def analyze_resume(jd_text, resume_text):
    prompt = f"""
You are an AI hiring assistant.

Compare the resume with the job description.

IMPORTANT RULES:
- Do NOT mention the candidate's name.
- Use neutral language like "The candidate".

Job Description:
{jd_text}

Resume:
{resume_text}

Respond STRICTLY in this format:

Score: <number between 0 and 100>
Skill Match: <percentage>
Strengths: <one concise sentence>
Missing Skills: <one concise sentence>
Recommendation: <Hire / Maybe / Reject>
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

def parse_result(text):
    data = {}
    for line in text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data

if analyze and jd_file and resume_files:
    jd_text = extract_text_from_pdf(jd_file)

    st.subheader("📊 Results")

    results = []

    for resume in resume_files:
        resume_text = extract_text_from_pdf(resume)

        with st.spinner(f"Analyzing {resume.name}..."):
            raw_result = analyze_resume(jd_text, resume_text)
            parsed = parse_result(raw_result)

        parsed["Candidate"] = resume.name
        parsed["Score"] = int(parsed.get("Score", 0))
        results.append(parsed)

results = sorted(results, key=lambda x: x["Score"], reverse=True)

st.subheader("🏆 Ranked Candidates")

st.info("📌 Candidates are ranked using AI-based semantic matching, not keyword search.")

for i, r in enumerate(results, start=1):
    if r["Recommendation"] == "Hire":
        color = "🟢"
    elif r["Recommendation"] == "Maybe":
        color = "🟡"
    else:
        color = "🔴"

    st.markdown(f"""
### {color} Rank #{i} — {r['Candidate']}
**Score:** {r['Score']}  
**Skill Match:** {r.get('Skill Match', '')}

**Strengths:**  
{r.get('Strengths', '')}

**Missing Skills:**  
{r.get('Missing Skills', '')}

**Final Recommendation:** **{r.get('Recommendation', '')}**
---
""")
