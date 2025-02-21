# Virtual Interviewer
[![Watch the video](assets/thumbnail.png)](assets/video.mp4)



**Virtual Interviewer** is an AI-powered platform designed to assist job seekers in preparing for interviews. It integrates several advanced technologies, including **ATS scoring**, **personalized interview questions generation**, and **voice input analysis**. Built using **Python**, **Streamlit**, and various NLP models, this tool provides valuable feedback to optimize resumes and improve interview responses.

---

## Features

- **ATS Compliance Scoring**: 
  - Analyze resumes to check for relevant keywords and assess ATS compatibility. 
  - Provides actionable feedback and suggestions to improve your resume.
  
- **Interview Question Generation**: 
  - Generate tailored interview questions based on your resume using the **Google Gemini API**.
  - Receive suggested answers for each question to help you prepare effectively.

- **Voice Input Analysis**: 
  - Practice virtual interviews with voice recognition.
  - Analyze speech for sentiment and emotional tone using **Hugging Face Transformers**.
  - Receive real-time feedback on your responses based on emotional positivity and keyword presence.

- **Streamlit Interface**: 
  - Easy-to-use web interface for uploading resumes, generating interview questions, and practicing voice responses.

---

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: For creating the interactive web app.
- **SpaCy**: For natural language processing and resume keyword extraction.
- **Google Gemini API**: For generating personalized interview questions.
- **SpeechRecognition**: For voice input analysis.
- **Hugging Face Transformers**: For sentiment and emotion analysis.

---

## Installation

### Prerequisites
- Python 3.7+
- Install required libraries:

```bash
pip install spacy streamlit PyPDF2 google-generativeai transformers SpeechRecognition
