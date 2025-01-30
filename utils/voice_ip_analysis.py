import os
import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import speech_recognition as sr
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load sentiment analysis model (fine-tuned for sentiment classification)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Define more nuanced emotion labels (based on sentiment scores)
emotion_labels = ["Negative", "Neutral", "Positive"]

def start_recording(sample_rate=16000):
    """Start recording audio."""
    duration = st.session_state.get("duration", 30)  # Default duration
    st.session_state["is_recording"] = True
    st.session_state["audio_data"] = sd.rec(
        int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype="int16"
    )
    st.info("Recording started. Speak now!")

def stop_recording(filename="output.wav"):
    """Stop recording and save audio file."""
    st.session_state["is_recording"] = False
    sd.stop()
    
    # Save recorded data to WAV file
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(st.session_state["audio_data"].tobytes())
        st.success(f"Recording saved successfully!")
    except Exception as e:
        st.error(f"Error saving recording: {e}")

def transcribe_audio(filename="output.wav"):
    """Convert recorded audio into text."""
    if not os.path.exists(filename):
        st.error("No audio file found. Please record your response first.")
        return None

    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Try speaking more clearly.")
            return None
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")
            return None

def analyze_response(text):
    """Analyze the response for sentiment and technical relevance."""
    if not text:
        return 0, 0, False

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    sentiment_score = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
    sentiment_label = sentiment_score.argmax().item()

    # Assign confidence & calmness based on sentiment
    if sentiment_label == 2:  # Positive sentiment
        calmness = round(float(sentiment_score[2]) * 0.8 + 0.2, 2)
        confidence = round(float(sentiment_score[2]) * 0.8 + 0.2, 2)
    elif sentiment_label == 1:  # Neutral sentiment
        calmness = 0.5
        confidence = 0.5
    else:  # Negative sentiment
        calmness = round(float(sentiment_score[0]) * 0.5, 2)
        confidence = round(float(sentiment_score[0]) * 0.5, 2)

    # Improved technical relevance detection
    technical_keywords = [
        "programming", "coding", "software", "developer", "engineer",
        "data", "machine learning", "AI", "project", "technology",
        "framework", "skills", "experience", "analysis", "database"
    ]
    relevance_score = sum(text.lower().count(keyword) for keyword in technical_keywords)
    relevance = relevance_score > 1  # More than 1 occurrence for better relevance detection

    return calmness, confidence, relevance

def voice_input_analysis():
    st.title("🎤 Virtual Technical Interview")
    st.markdown("### Speak about yourself or answer the interview question:")

    if "is_recording" not in st.session_state:
        st.session_state["is_recording"] = False
        st.session_state["audio_data"] = None
        st.session_state["duration"] = 30  # Default recording duration

    # Recording controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎙️ Start Recording") and not st.session_state["is_recording"]:
            start_recording()
    with col2:
        if st.button("⏹️ Stop Recording") and st.session_state["is_recording"]:
            stop_recording()

    # Process and analyze audio
    if st.button("📄 Submit Response"):
        st.info("Processing your response...")
        text = transcribe_audio()
        if text:
            st.markdown(f"### **Transcription:**\n{text}")

            calmness, confidence, relevance = analyze_response(text)

            st.subheader("🔎 Interview Feedback")
            st.write(f"🧘 **Calmness:** `{calmness * 100:.1f}%`")
            st.write(f"💪 **Confidence:** `{confidence * 100:.1f}%`")
            st.write(f"📌 **Relevance to Technical Topics:** `{'Yes' if relevance else 'No'}`")

            if calmness > 0.4 and confidence > 0.4 and relevance:
                st.success("✅ Great job! You performed well in the interview.")
            else:
                st.error("❌ You need improvement. Focus on staying calm, confident, and relevant to technical topics.")

            # Additional guidance
            st.markdown("### Tips for Improvement:")
            if calmness < 0.4:
                st.markdown("- **Try speaking at a steady pace** and avoid rushing.")
            if confidence < 0.4:
                st.markdown("- **Structure your response clearly** and avoid long pauses.")
            if not relevance:
                st.markdown("- **Mention technical keywords** and highlight relevant experience.")
