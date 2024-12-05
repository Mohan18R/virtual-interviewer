import streamlit as st
from utils.pdf_process import extract_text_from_pdf
from utils.ats_scorer import evaluate_ats
from utils.question_gen import generate_questions_with_gemini
# from utils.save_QNA import save_qna_to_txt
from utils.voice_ip_analysis import voice_input_analysis

def main():
    st.title("Virtual Interviewer")
     # Display Image
    image_path = "image.png"  # Provide the correct path to your image file
    st.image(image_path, caption="virtual interviewer", use_column_width=True)
    st.markdown(
        """
        **Features:**
        - Upload and evaluate your resume for ATS compliance.
        - Generate interview questions tailored to your resume.
        - Practice virtual interviews with voice analysis.
        """
    )

    # Step 1: Upload Resume
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")
    if uploaded_file:
        pdf_text = extract_text_from_pdf(uploaded_file)

        # ATS Scoring
        st.subheader("ATS Compliance Scoring")
        if st.button("Evaluate Resume (ATS Scoring)", key="ats_score_button"):
            with st.spinner("Evaluating ATS compliance..."):
                ats_score, feedback = evaluate_ats(pdf_text)
            st.success("Evaluation Complete!")
            
            # Display ATS Score
            st.markdown(f"### ATS Score: **{ats_score}/100**")
            st.progress(ats_score/100)
            st.markdown(f"#### Feedback:")
            st.write(feedback)

        # Generate Interview Questions
        st.subheader("Generate Interview Questions & Answers")
        if st.button("Generate Interview Questions & Answers", key="generate_qna_button"):
            with st.spinner("Generating interview questions and answers..."):
                questions_answers = generate_questions_with_gemini(pdf_text)
            
            if questions_answers:
                st.success("Questions and answers generated successfully!")
                for i, qa in enumerate(questions_answers, start=1):
                    st.markdown(f"** {qa['question']}**")
                    st.write(f"**Answer:** {qa['answer']}")
                
               
            else:
                st.error("Unable to generate questions and answers. Ensure your resume contains detailed information.")

    # Virtual Interview Voice Analysis
    st.subheader("Virtual Interview Practice")
    if st.button("Start Virtual Interview"):
        voice_input_analysis()

if __name__ == "__main__":
    main()
