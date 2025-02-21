import streamlit as st
# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Virtual Interviewer AI",
    page_icon="🎙️",
    layout="wide"
)

from utils.pdf_process import extract_text_from_pdf
from utils.ats_scorer import evaluate_ats
from utils.question_gen import generate_questions_with_gemini
from utils.voice_ip_analysis import voice_input_analysis
from utils.ui_enhancements import (
    load_custom_css,
    show_loading_animation,
    display_score_meter,
    create_animated_timeline
)

def main():
    # Load custom CSS and configurations
    load_custom_css()

    # Create two columns for header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🎙️ Virtual Interviewer AI")
        st.markdown("*Your personal interview preparation assistant*")
    with col2:
        st.markdown("""
            <div class="golden-frame">
                <img src="https://i.pinimg.com/736x/bf/48/d2/bf48d2ec10d4ed9df964d5559da11221.jpg" alt="Virtual Interviewer">
            </div>
        """, unsafe_allow_html=True)

    # Create tabs for different features
    tabs = st.tabs(["🏠 Home", "📂 Resume Analysis", "🎯 Interview Practice"])

    # Home Tab
    with tabs[0]:
        st.markdown("""
        <div class="highlight-box">
            <h2>Welcome to Virtual Interviewer AI! 👋</h2>
            <p>Prepare for your next interview with confidence using our AI-powered tools.</p>
        </div>
        """, unsafe_allow_html=True)

        # Feature cards in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="feature-card-new">
                <div class="icon">📊</div>
                <h3>ATS Analysis</h3>
                <p>Get your resume scored and optimized for ATS systems</p>
                <ul>
                    <li>Keyword optimization</li>
                    <li>Format checking</li>
                    <li>Section analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="feature-card-new">
                <div class="icon">🤖</div>
                <h3>AI Questions</h3>
                <p>Receive personalized interview questions based on your resume</p>
                <ul>
                    <li>Technical questions</li>
                    <li>Behavioral scenarios</li>
                    <li>Role-specific prep</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="feature-card-new">
                <div class="icon">🎤</div>
                <h3>Voice Analysis</h3>
                <p>Practice interviews with real-time voice feedback</p>
                <ul>
                    <li>Confidence scoring</li>
                    <li>Speech clarity</li>
                    <li>Pace analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # Resume Analysis Tab
    with tabs[1]:
        st.subheader("📂 Upload Your Resume")
        uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")
        
        if uploaded_file:
            pdf_text = extract_text_from_pdf(uploaded_file)

            col1, col2 = st.columns(2)
            
            # ATS Scoring Section
            with col1:
                st.markdown("""
                <div class="section-card">
                    <h3>📊 ATS Compliance Score</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Evaluate Resume"):
                    show_loading_animation()
                    ats_score, feedback = evaluate_ats(pdf_text)
                    
                    display_score_meter(ats_score)
                    st.markdown("### 📝 Detailed Feedback")
                    st.markdown(feedback)

            # Interview Questions Generation
            with col2:
                st.markdown("""
                <div class="section-card">
                    <h3>🎯 Interview Questions</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Generate Questions"):
                    show_loading_animation()
                    questions_answers = generate_questions_with_gemini(pdf_text)
                    
                    if questions_answers:
                        for i, qa in enumerate(questions_answers, start=1):
                            with st.expander(f"Q{i}: {qa['question']}"):
                                st.write(f"**Suggested Answer:** {qa['answer']}")
                    else:
                        st.error("⚠️ Unable to generate questions. Please try again.")

    # Interview Practice Tab
    with tabs[2]:
        st.subheader("🎤 Virtual Interview Practice")
        st.markdown("""
        <div class="feature-card-new practice-section">
            <div class="icon">🎯</div>
            <h3>Practice Interview Session</h3>
            <p>Practice your interview skills with real-time voice analysis</p>
            <ul>
                <li>Get instant feedback on your responses</li>
                <li>Analyze speech clarity and confidence</li>
                <li>Track your improvement over time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            voice_input_analysis()

if __name__ == "__main__":
    main()
