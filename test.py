from resume_parser import extract_text_from_pdf
from scoring import clean_text, calculate_similarity

# read resume
with open("sample_resume.pdf", "rb") as f:
    resume_text = extract_text_from_pdf(f)

# sample job description
job_desc = """
Looking for a Python developer with knowledge of machine learning,
data structures, SQL, and web development.
"""

# clean both
clean_resume = clean_text(resume_text)
clean_job = clean_text(job_desc)

# calculate score
score = calculate_similarity(clean_resume, clean_job)

print("MATCH SCORE:", score, "%")