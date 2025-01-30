import spacy
from collections import Counter
from spacy.matcher import PhraseMatcher
import re

# Load SpaCy model with word vectors
nlp = spacy.load("en_core_web_sm")  # Use "md" or "lg" model for better similarity

# Define target keywords with weights
target_keywords = {
    "teamwork": 1, 
    "leadership": 1, 
    "project management": 2, 
    "python": 3, 
    "data analysis": 2.5,
    "java": 2, 
    "machine learning": 3,
    "communication": 1.5,
    "artificial intelligence": 3,
    "problem-solving": 1.5
}

# Synonyms for broader matching
keyword_synonyms = {
    "teamwork": ["collaboration", "team player"],
    "leadership": ["mentorship", "guidance"],
    "project management": ["agile", "scrum", "kanban"],
    "python": ["Python3", "Django", "Flask"],
    "data analysis": ["data science", "data visualization"],
    "java": ["Spring", "JavaEE"],
    "machine learning": ["deep learning", "neural networks"],
    "communication": ["presentation", "public speaking"],
    "artificial intelligence": ["AI", "computer vision", "NLP"],
    "problem-solving": ["critical thinking", "troubleshooting"]
}

# Convert keywords and synonyms into phrase matcher patterns
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
for keyword, synonyms in keyword_synonyms.items():
    patterns = [nlp(text) for text in [keyword] + synonyms]
    matcher.add(keyword, patterns)

def extract_experience(text):
    """Extracts years of experience from resume text."""
    experience_patterns = re.findall(r"(\d+)\s*(?:\+|years|yrs|year|y)\s*(?:experience|exp)", text, re.IGNORECASE)
    return max(map(int, experience_patterns), default=0)  # Return highest found experience

def evaluate_ats(resume_text):
    """Enhanced ATS compliance scorer for resumes."""
    doc = nlp(resume_text.lower())

    # Find matches using PhraseMatcher
    found_keywords = [nlp.vocab.strings[match_id] for match_id, start, end in matcher(doc)]
    keyword_count = Counter(found_keywords)

    # Compute semantic similarity for unmatched words
    for token in doc:
        for key, weight in target_keywords.items():
            if token.text not in keyword_count and token.has_vector:
                similarity = token.similarity(nlp(key))
                if similarity > 0.75:  # Threshold for relevance
                    keyword_count[key] += 1

    # Extract years of experience
    years_of_experience = extract_experience(resume_text)

    # Section-based weighting
    experience_boost = 1.5 if "experience" in resume_text.lower() else 1.0

    # Calculate weighted ATS score
    weighted_score = sum(keyword_count[key] * target_keywords[key] * experience_boost for key in keyword_count)
    max_possible_score = sum(target_keywords.values()) * 2  
    ats_score = min((weighted_score / max_possible_score) * 100, 100)  # Scale to 100

    ats_score = round(ats_score, 2)

    # Feedback generation
    feedback = f"**Keywords Found:**\n"
    feedback += ", ".join([f"**{key}** ({keyword_count[key]})" for key in keyword_count]) + "\n\n"

    missing_keywords = set(target_keywords.keys()) - set(keyword_count.keys())
    if missing_keywords:
        feedback += f"**Missing Keywords:** {', '.join(missing_keywords)}\n\n"
    else:
        feedback += "**Great job! Your resume covers all critical keywords.**\n\n"

    # ATS Formatting Compliance Checks
    if any(tag in resume_text.lower() for tag in ["table", "<table>", "pdf"]):
        feedback += "⚠️ **Warning:** Your resume may contain tables or non-ATS-friendly formatting. Use simple text formatting.\n\n"
    
    feedback += f"**Years of Experience Detected:** {years_of_experience} years\n\n"
    feedback += "**Additional Suggestions:**\n- Tailor your resume to highlight achievements.\n- Optimize formatting for ATS parsing."

    return ats_score, feedback
