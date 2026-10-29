
import streamlit as st
from backend import read_resume, calculate_score, find_matching_jobs

st.set_page_config(
    page_title="AI Based Resume Analyser",
    page_icon="📄",
    layout="wide"
)

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_filename" not in st.session_state:
    st.session_state.resume_filename = ""

if "resume_score" not in st.session_state:
    st.session_state.resume_score = None

if "matching_jobs" not in st.session_state:
    st.session_state.matching_jobs = None

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f3ff, #eef7ff);
}
.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}
h1 {
    color: #5138a5;
}
div.stButton > button {
    border-radius: 10px;
    min-height: 45px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Based Resume Analyser")
st.write("Analyse your resume, check your skills, and discover suitable jobs.")
st.caption("Python-powered resume reading and job matching")
st.divider()

st.subheader("📤 1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose a PDF or DOCX resume",
    type=["pdf", "docx"],
    key="resume_upload"
)

if uploaded_file is not None:
    st.success("Selected: " + uploaded_file.name)

st.subheader("🛠️ Resume Tools")

# Button 1: Upload Resume
if st.button("📂 Upload Resume", use_container_width=True):
    if uploaded_file is None:
        st.warning("Please select a resume first.")
    else:
        st.session_state.resume_filename = uploaded_file.name
        st.session_state.resume_text = ""
        st.session_state.resume_score = None
        st.session_state.matching_jobs = None
        st.success("Resume selected successfully. Now click Read Resume File.")

# Button 2: Read Resume File
if st.button("📖 Read Resume File", use_container_width=True):
    if uploaded_file is None:
        st.warning("Please select a PDF or DOCX file first.")
    else:
        try:
            with st.spinner("Reading resume..."):
                text = read_resume(uploaded_file)

            st.session_state.resume_text = text
            st.session_state.resume_filename = uploaded_file.name
            st.session_state.resume_score = None
            st.session_state.matching_jobs = None

            st.success("Resume text extracted successfully!")

        except Exception as error:
            st.error("Could not read resume: " + str(error))

# Button 3: Resume Score
if st.button("📊 Resume Score", use_container_width=True):
    if not st.session_state.resume_text:
        st.warning("First upload and read your resume.")
    else:
        st.session_state.resume_score = calculate_score(
            st.session_state.resume_text
        )
        st.success("Resume score calculated.")

# Button 4: Find Matching Jobs
if st.button("🎯 Find Matching Jobs", use_container_width=True):
    if not st.session_state.resume_text:
        st.warning("First upload and read your resume.")
    else:
        st.session_state.matching_jobs = find_matching_jobs(
            st.session_state.resume_text
        )
        st.success("Job matching completed.")

# Buttons 5–7 remain inactive
st.button("🧠 Skill Analysis", disabled=True, use_container_width=True)
st.button("📑 View Full Analysis Report", disabled=True, use_container_width=True)
st.button("🔄 Clear/Reset", disabled=True, use_container_width=True)

st.divider()
st.header("📋 Resume Results")

if st.session_state.resume_text:
    st.subheader("📄 Extracted Resume")
    st.caption("File: " + st.session_state.resume_filename)

    st.text_area(
        "Resume text",
        value=st.session_state.resume_text,
        height=250,
        disabled=True
    )

if st.session_state.resume_score is not None:
    score = st.session_state.resume_score

    st.subheader("⭐ Resume Score")
    st.progress(score / 100)

    col1, col2 = st.columns(2)
    col1.metric("Skill Coverage", str(score) + "%")

    if score >= 70:
        col2.success("Strong coverage of predefined skills")
    elif score >= 40:
        col2.info("Some relevant skills detected")
    else:
        col2.warning("Consider adding relevant skills")

    st.caption(
        "This is a rule-based skill coverage score, not an overall "
        "professional resume-quality assessment."
    )

if st.session_state.matching_jobs is not None:
    st.subheader("💼 Matching Job Recommendations")

    for job in st.session_state.matching_jobs:
        with st.container(border=True):
            st.markdown("### " + job["title"])

            st.metric("Job Skill Match", str(job["match"]) + "%")
            st.progress(job["match"] / 100)

            st.write(
                "**Matched skills:** "
                + (", ".join(job["matched"]) if job["matched"] else "None")
            )

            st.write(
                "**Missing skills:** "
                + (", ".join(job["missing"]) if job["missing"] else "None")
            )

st.divider()
st.caption("AI Based Resume Analyser | Developed using Python")
