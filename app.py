                      max(1, len(set(re.findall(r"[a-zA-Z]{4,}", job_description.lower())))))
        ),
    }
    return sum(categories.values()), categories


def get_gemini_feedback(api_key: str, resume_text: str, job_description: str) -> str:
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an expert resume coach. Review the resume and, if provided, compare it with the job description.
Be honest, specific, actionable, and evidence-based. Never invent candidate experience, skills,
qualifications, employers, dates, metrics, or achievements. If information is missing, say so.
Do not claim to know or reproduce the scoring rules of any employer's ATS.

Return Markdown with these exact sections:
### Overall assessment
### Top 5 improvements (prioritized)
### Suggested summary rewrite
### Stronger bullet examples
### Keywords to consider (only if supported by the candidate's experience)
### Formatting and ATS tips

For bullet examples, rewrite only information supported by the resume. Use placeholders such as [add metric]
where a real number is needed. If no job description is supplied, give general resume advice.

RESUME:
{resume_text[:MAX_TEXT_CHARS]}

JOB DESCRIPTION:
{job_description[:8000] if job_description.strip() else "Not provided"}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1800,
        ),
    )
    answer = (response.text or "").strip()
    if not answer:
        raise RuntimeError("Gemini returned an empty response. Please try again.")
    return answer


with st.sidebar:
    st.header("Settings")
    st.caption(f"Gemini model: `{MODEL_NAME}`")
    try:
        saved_api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        saved_api_key = ""
    api_key = st.text_input(
        "Google Gemini API key",
        type="password",
        value=saved_api_key or os.getenv("GEMINI_API_KEY", ""),
        help="Stored only for this session unless you add it to Streamlit Secrets.",
    )
    st.caption("Get an API key from Google AI Studio. Never commit your key to GitHub.")

uploaded = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
job_description = st.text_area(
    "Job description (optional)",
    placeholder="Paste the job description here for a more targeted comparison...",
    height=180,
)

if uploaded:
    size_mb = len(uploaded.getvalue()) / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        st.error(f"File is too large. Maximum size is {MAX_FILE_MB} MB.")
        st.stop()
    try:
        resume_text = extract_resume(uploaded)
    except Exception as exc:
        st.error(f"Could not read this file: {exc}")
        st.stop()

    if not resume_text:
        st.warning("No selectable text was found. If this is a scanned PDF, run OCR on it or upload a text-based PDF/DOCX.")
        st.stop()

    st.success(f"Resume loaded: {uploaded.name}")
    with st.expander("Preview extracted resume text"):
        st.text(resume_text[:5000])

    if st.button("Analyze my resume", type="primary", use_container_width=True):
        if not api_key.strip():
            st.error("Add your Gemini API key in the sidebar or Streamlit Secrets.")
        else:
            score, breakdown = heuristic_score(resume_text, job_description)
            with st.spinner("Gemini is reviewing your resume..."):
                try:
                    feedback = get_gemini_feedback(api_key.strip(), resume_text, job_description)
                except Exception as exc:
                    st.error(f"Gemini analysis failed: {exc}")
                    st.stop()

            st.divider()
            st.subheader("Estimated ATS-readiness score")
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Heuristic estimate", f"{score}/100")
                st.caption("A transparent checklist estimate, not a real ATS vendor score or hiring prediction.")
            with c2:
                st.write("Score breakdown")
                for label, points in breakdown.items():
                    st.write(f"**{label}:** {points}")
                    st.progress(points / (15 if label in ["Contact information", "Education", "Skills", "Readable structure"] else 20 if label == "Work experience" else 10))
            st.divider()
            st.subheader("AI improvement report")
            st.markdown(feedback)
            st.download_button(
                "Download feedback as Markdown",
                data=f"# ATS Resume Analysis\n\nEstimated score: {score}/100\n\n"
                     f"## Score breakdown\n{json.dumps(breakdown, indent=2)}\n\n{feedback}",
                file_name="resume_feedback.md",
                mime="text/markdown",
            )
else:
    st.info("Upload a PDF, DOCX, or TXT resume to begin.")

st.caption("Privacy: resume text is sent to Google's Gemini API when you click Analyze. Avoid uploading documents containing information you do not want processed.")
