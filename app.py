import streamlit as st
from resume_parser import extract_text_from_pdf
from scoring import clean_text, calculate_similarity, skill_match, advanced_score

# Page config
st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="centered")

# ----------- CUSTOM UI STYLE -----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1 {
    text-align: center;
    color: #00c6ff;
}
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.markdown("<h1>AI Resume Matcher</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Analyze how well your resume matches a job description using AI</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------- INPUT SECTION -----------
st.subheader("📤 Upload Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

st.subheader("📝 Job Description")
job_desc = st.text_area("Paste the job description here", height=150)

# ----------- BUTTON ACTION -----------
if st.button("🚀 Analyze Match"):

    if uploaded_file is None or job_desc.strip() == "":
        st.warning("⚠️ Please upload a resume and enter job description")

    else:
        with st.spinner("Analyzing... 🤖"):

            # Extract text
            resume_text = extract_text_from_pdf(uploaded_file)

            # Clean text
            clean_resume = clean_text(resume_text)
            clean_job = clean_text(job_desc)

            # Scores
            base_score = calculate_similarity(clean_resume, clean_job)
            matched, missing = skill_match(clean_resume, clean_job)
            score = advanced_score(base_score, matched, len(matched) + len(missing))

        # ----------- RESULT -----------
        st.subheader("📊 Match Result")
        st.progress(int(score))
        st.markdown(f"<h2 style='text-align:center; color:#00c6ff;'>Match Score: {score}%</h2>", unsafe_allow_html=True)

        # Status
        if score > 70:
            st.success("✅ Strong Match!")
        elif score > 40:
            st.warning("⚠️ Average Match")
        else:
            st.error("❌ Low Match")

        # ----------- IMPROVEMENTS -----------
        st.subheader("💡 Resume Improvement Suggestions")

        if score > 70:
            st.success("Your resume is well aligned with the job.")
            st.write("👉 Add more measurable achievements (e.g., improved performance by 20%).")
            st.write("👉 Include advanced tools or frameworks to stand out.")
            st.write("👉 Keep updating projects with real-world impact.")

        elif score > 40:
            st.warning("Your resume partially matches the job description.")

            if missing:
                st.write("👉 Consider adding these skills:")
                st.write(", ".join(missing))

            st.write("👉 Improve project descriptions with more technical depth.")
            st.write("👉 Highlight tools like pandas, numpy, scikit-learn.")
            st.write("👉 Add more AI/ML-related experience if applying for such roles.")

        else:
            st.error("Your resume has low alignment with the job description.")

            if missing:
                st.write("👉 You should learn and add these key skills:")
                st.write(", ".join(missing))

            st.write("👉 Build projects related to this job role.")
            st.write("👉 Add relevant keywords from the job description.")
            st.write("👉 Focus on core skills required for this position.")

# ----------- FOOTER -----------
st.markdown("""
<hr>
<p style='text-align:center; color:gray;'>
AI Resume Matcher
</p>
""", unsafe_allow_html=True)
# Git author verification