import google.generativeai as genai
import os

def generate_questions_with_gemini(resume_text):
    """
    Generate interview questions and suggested answers based on a resume using the Google Gemini API.
    """
    genai.configure(api_key="GEMINI API KEY")  # Replace with your actual API key

    prompt = f"""
    You are a professional interviewer reviewing the following resume details:

    {resume_text}

    Based on this resume, generate **exactly 5 interview questions** related to the candidate's experience, skills, 
    and achievements. For each question, also provide a well-structured suggested answer.

    Format your response strictly as:
    
    Q1: <Question 1>
    A1: <Suggested Answer 1>
    
    Q2: <Question 2>
    A2: <Suggested Answer 2>
    
    Q3: <Question 3>
    A3: <Suggested Answer 3>
    
    Q4: <Question 4>
    A4: <Suggested Answer 4>
    
    Q5: <Question 5>
    A5: <Suggested Answer 5>
    """

    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)

        # Ensure valid response text
        if not response.text:
            return [{"question": "Error", "answer": "No response received from Gemini API"}]

        # Extract questions and answers correctly
        lines = response.text.split("\n")
        questions_answers = []
        for i in range(1, 6):  # Expecting 5 Q&A pairs
            q_key = f"Q{i}:"
            a_key = f"A{i}:"
            q_text = next((line.replace(q_key, "").strip() for line in lines if line.startswith(q_key)), None)
            a_text = next((line.replace(a_key, "").strip() for line in lines if line.startswith(a_key)), None)
            if q_text and a_text:
                questions_answers.append({"question": q_text, "answer": a_text})

        return questions_answers if questions_answers else [{"question": "Error", "answer": "Invalid response format"}]

    except Exception as e:
        return [{"question": "API Error", "answer": str(e)}]
