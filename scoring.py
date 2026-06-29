import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def calculate_similarity(resume, job_desc):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, job_desc])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(similarity[0][0] * 100, 2)

def extract_skills(text):
    skills_db = [
        "python", "sql", "machine learning", "data structures",
        "html", "css", "c", "numpy", "pandas", "scikit learn"
    ]

    doc = nlp(text)
    found = []

    for token in doc:
        if token.text.lower() in skills_db:
            found.append(token.text.lower())

    return list(set(found))

def skill_match(resume, job_desc):
    resume_skills = set(extract_skills(resume))
    job_skills = set(extract_skills(job_desc))

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    return list(matched), list(missing)

def advanced_score(similarity, matched, total_skills):
    if total_skills == 0:
        return similarity

    skill_score = (len(matched) / total_skills) * 100
    final_score = (0.7 * similarity) + (0.3 * skill_score)

    return round(final_score, 2)