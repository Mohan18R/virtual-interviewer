import streamlit as st
import speech_recognition as sr
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# Load NLP models for sentiment and emotion analysis
sentiment_analyzer = pipeline("sentiment-analysis")  # Hugging Face Sentiment Analysis
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

# Define emotion labels
emotion_labels = ["calm", "anxious", "confident", "joyful", "sad"]

def analyze_response(text):
    # Sentiment Analysis
    sentiment = sentiment_analyzer(text)[0]

    # Emotional tone detection
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    emotion_scores = outputs.logits.softmax(dim=-1).detach().numpy()[0]
    emotion_data = {label: score for label, score in zip(emotion_labels, emotion_scores)}

    # Keyword Matching
    keywords = ["experience", "skills", "goal", "passion"]
    keyword_count = sum(1 for keyword in keywords if keyword in text.lower())

    # Extract Emotion Scores
    calmness = emotion_data.get("calm", 0)
    confidence = emotion_data.get("confident", 0)
    positivity = calmness + confidence  # Give combined weight to calmness and confidence.

    # Passing Criteria
    passed = (positivity > 1.2) or (calmness > 0.6 and confidence > 0.6) or (keyword_count >= 1)
    return sentiment, emotion_data, passed

def voice_input_analysis():
    st.subheader("Speak about yourself for the virtual interview:")

    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Please speak clearly.")
            try:
                # Capture and process audio
                audio_data = recognizer.listen(source, timeout=10)
                st.success("Recording complete! Processing your response...")

                # Transcribe the audio
                text = recognizer.recognize_google(audio_data)
                
                # AI Analysis
                _, _, passed = analyze_response(text)

                # Display Results
                st.subheader("Transcription:")
                st.write(text)
                if passed:
                    st.success("Congratulations! You passed the interview.")
                else:
                    st.error("Unfortunately, you did not pass the interview. Try to improve your response.")
            except sr.UnknownValueError:
                st.error("Could not understand your voice. Please try again.")
            except sr.RequestError as e:
                st.error(f"Speech recognition service is unavailable: {e}")
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
