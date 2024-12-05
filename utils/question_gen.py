import google.generativeai as genai
import os
def generate_questions_with_gemini(resume_text):
    """
    Generate interview questions and suggested answers based on resume using Google Gemini API.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    prompt = f"""
    You are a professional interviewer. Based on the following resume details, generate 5 interview questions 
    and provide suggested answers for each question in a well-organized format:

    {resume_text}
    """

    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        # Split and format response into questions and answers
        questions_answers = [
            {"question": qa.split(":")[0], "answer": qa.split(":")[1]}
            for qa in response.text.split("\n") if ":" in qa
        ]
        return questions_answers
    except Exception as e:
        return [{"question": "Error generating questions", "answer": str(e)}]
