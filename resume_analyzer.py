import re
import json

# Sample resume text
resume_text = """
Name: Tanya Agarwal
Email: tanya123@gmail.com
Skills: Python, SQL, Power BI, Excel, Data Analysis
Experience: 2 years
"""

# Job required skills
job_skills = ["Python", "SQL", "Machine Learning", "Power BI"]

# Skills database
skill_database = [
    "Python", "SQL", "Power BI", "Excel",
    "Machine Learning", "Data Analysis", "Tableau"
]


def extract_name(text):
    """Extract candidate name from resume."""
    for line in text.split("\n"):
        if "Name:" in line:
            return line.split(":")[1].strip()
    return "Not Found"


def extract_email(text):
    """Extract email using regex."""
    pattern = r'\S+@\S+'
    match = re.search(pattern, text)
    return match.group() if match else "Not Found"


def extract_skills(text, skills):
    """Identify skills present in resume."""
    found = []
    for skill in skills:
        if skill.lower() in text.lower():
            found.append(skill)
    return found


def extract_experience(text):
    """Extract years of experience."""
    pattern = r'(\d+)\s+years'
    match = re.search(pattern, text.lower())
    return int(match.group(1)) if match else 0


def calculate_match(candidate_skills, required_skills):
    """Calculate skill match score."""
    if not required_skills:
        return 0

    matched = set(candidate_skills).intersection(required_skills)
    score = (len(matched) / len(required_skills)) * 100
    return round(score)


def generate_recommendation(score):
    """Generate hiring recommendation."""
    if score >= 70:
        return "Highly Recommended"
    elif score >= 40:
        return "Recommended"
    return "Not Recommended"


try:
    # Resume Parsing
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    skills = extract_skills(resume_text, skill_database)
    experience = extract_experience(resume_text)

    # Match Score Calculation
    match_score = calculate_match(skills, job_skills)

    # Recommendation
    recommendation = generate_recommendation(match_score)

    # Store results
    candidate_data = {
        "name": name,
        "email": email,
        "skills": skills,
        "experience": experience,
        "match_score": match_score,
        "recommendation": recommendation
    }

    # Save to JSON
    with open("analysis.json", "w") as file:
        json.dump(candidate_data, file, indent=4)

    # Load JSON for verification
    with open("analysis.json", "r") as file:
        saved_data = json.load(file)

    # Report Generation
    print("\n========== Resume Analysis Report ==========")
    print("Candidate Name:", saved_data["name"])
    print("Email:", saved_data["email"])
    print("Skills Identified:", saved_data["skills"])
    print("Experience:", saved_data["experience"], "years")
    print("Match Score:", saved_data["match_score"], "/ 100")
    print("Hiring Recommendation:", saved_data["recommendation"])
    print("============================================")

except Exception as error:
    print("Error processing resume:", error)