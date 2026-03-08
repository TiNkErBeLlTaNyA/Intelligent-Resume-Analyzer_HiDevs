import re
import json

# Job required skills
job_skills = ["Python", "SQL", "Machine Learning", "Power BI"]

# Skills database
skill_database = [
    "Python", "SQL", "Power BI", "Excel",
    "Machine Learning", "Data Analysis", "Tableau"
]

# -------- USER INPUT --------
name_input = input("Enter candidate name: ")
email_input = input("Enter email: ")
skills_input = input("Enter skills (comma separated): ")
experience_input = input("Enter years of experience: ")

# Create resume text
resume_text = f"""
Name: {name_input}
Email: {email_input}
Skills: {skills_input}
Experience: {experience_input} years
"""


def extract_name(text):
    for line in text.split("\n"):
        if "Name:" in line:
            return line.split(":")[1].strip()
    return "Not Found"


def extract_email(text):
    pattern = r'\S+@\S+'
    match = re.search(pattern, text)
    return match.group() if match else "Not Found"


def extract_skills(text, skills):
    found = []
    for skill in skills:
        if skill.lower() in text.lower():
            found.append(skill)
    return found


def extract_experience(text):
    pattern = r'(\d+)\s+years'
    match = re.search(pattern, text.lower())
    return int(match.group(1)) if match else 0


def calculate_match(candidate_skills, required_skills, experience):
    matched = set(candidate_skills).intersection(required_skills)
    skill_score = (len(matched) / len(required_skills)) * 100
    experience_score = min(experience * 5, 20)
    final_score = skill_score * 0.8 + experience_score
    return round(final_score)


def generate_recommendation(score):
    if score >= 70:
        return "Highly Recommended"
    elif score >= 40:
        return "Consider for Interview"
    else:
        return "Not Recommended"


try:

    # Resume Parsing
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    skills = extract_skills(resume_text, skill_database)
    experience = extract_experience(resume_text)

    # Match Score
    match_score = calculate_match(skills, job_skills, experience)

    # Recommendation
    recommendation = generate_recommendation(match_score)

    # Candidate data
    candidate_data = {
        "name": name,
        "email": email,
        "skills": skills,
        "experience": experience,
        "match_score": match_score,
        "recommendation": recommendation
    }

    # -------- LOAD OLD DATA --------
    try:
        with open("analysis.json", "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except:
        data = []

    # -------- ADD NEW CANDIDATE --------
    data.append(candidate_data)

    # -------- SORT BY MATCH SCORE --------
    data.sort(key=lambda x: x["match_score"], reverse=True)

    # -------- SAVE AGAIN --------
    with open("analysis.json", "w") as file:
        json.dump(data, file, indent=4)

    # -------- PRINT ALL CANDIDATES --------
    print("\n========== All Candidate Analysis ==========")

    for candidate in data:
        print("\nName:", candidate["name"])
        print("Email:", candidate["email"])
        print("Skills:", candidate["skills"])
        print("Experience:", candidate["experience"], "years")
        print("Match Score:", candidate["match_score"], "/100")
        print("Recommendation:", candidate["recommendation"])
        print("----------------------------------")

except Exception as error:
    print("Error processing resume:", error)