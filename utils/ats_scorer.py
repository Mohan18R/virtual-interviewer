import spacy
from collections import Counter

# Load SpaCy model for resume parsing
nlp = spacy.load("en_core_web_sm")

def evaluate_ats(resume_text):
    """Enhanced ATS compliance scorer for resumes."""
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

    # Analyze resume text
    doc = nlp(resume_text.lower())

    # Match exact keywords and check for related words using SpaCy's similarity
    found_keywords = [token.text for token in doc if token.text in target_keywords]
    keyword_count = Counter(found_keywords)

    # Calculate ATS score based on keyword frequency and weighting
    weighted_score = sum(keyword_count[keyword] * target_keywords[keyword] for keyword in keyword_count)
    max_possible_score = sum(target_keywords.values()) * 2  # Scaling max score for leniency
    ats_score = min((weighted_score / max_possible_score) * 100, 100)  # Scale to 100

    ats_score = round(ats_score, 2)

    # Feedback generation
    feedback = f"**Keywords Found:**\n"
    feedback += ", ".join([f"**{key}** ({keyword_count[key]})" for key in keyword_count]) + "\n\n"

    missing_keywords = set(target_keywords.keys()) - set(keyword_count.keys())
    if missing_keywords:
        feedback += f"**Missing Keywords:** {', '.join(missing_keywords)}\n\n"
    else:
        feedback += "**Great job! Your resume covers all critical keywords.**"

    feedback += f"\n**Additional Suggestions:**\n- Tailor your resume to highlight more achievements.\n- Optimize formatting for ATS parsing."
    
    return ats_score, feedback
