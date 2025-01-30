import streamlit as st
from utils.pdf_process import extract_text_from_pdf
from utils.ats_scorer import evaluate_ats
from utils.question_gen import generate_questions_with_gemini
from utils.voice_ip_analysis import voice_input_analysis

def main():
    st.title("🎙️ Virtual Interviewer")
    
    # Display Logo or Banner Image
    image_path = "image.png"  # Ensure correct image path
    st.image(image_path, caption="Your AI Interview Assistant", use_column_width=True)

    # Feature Overview
    st.markdown(
        """
        ### 🚀 Features:
        ✅ Upload and **evaluate your resume** for ATS compliance.  
        ✅ Get **custom interview questions** tailored to your resume.  
        ✅ **Practice virtual interviews** with real-time voice analysis.  
        """
    )

    # Step 1: Resume Upload
    st.divider()
    st.subheader("📂 Upload Your Resume")
    
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")
    
    if uploaded_file:
        pdf_text = extract_text_from_pdf(uploaded_file)

        # ATS Scoring Section
        st.subheader("📊 ATS Compliance Scoring")
        if st.button("Evaluate Resume (ATS Scoring)"):
            with st.spinner("🔎 Evaluating ATS compliance..."):
                ats_score, feedback = evaluate_ats(pdf_text)
                
            st.success("✅ Evaluation Complete!")
            st.markdown(f"### 🏆 ATS Score: **{ats_score}/100**")
            st.progress(ats_score / 100)  # Visual progress bar
            st.markdown(f"#### 📌 Feedback:")
            st.write(feedback)

        # Interview Questions Generation
        st.subheader("📝 Generate Interview Questions & Answers")
        if st.button("Generate Interview Q&A"):
            with st.spinner("🤖 Generating AI-powered interview questions..."):
                questions_answers = generate_questions_with_gemini(pdf_text)
            
            if questions_answers:
                st.success("🎯 Questions and answers generated successfully!")
                for i, qa in enumerate(questions_answers, start=1):
                    st.markdown(f"**Q{i}: {qa['question']}**")
                    st.write(f"**Answer:** {qa['answer']}")
            else:
                st.error("⚠️ Unable to generate questions. Ensure your resume has sufficient content.")

    # Virtual Interview Voice Analysis
    st.divider()
    st.subheader("🎤 Virtual Interview Practice")
    voice_input_analysis()

if __name__ == "__main__":
    main()
