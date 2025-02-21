import streamlit as st
import time
from typing import List, Dict

def show_loading_animation():
    """Show a custom loading animation."""
    with st.spinner('Analyzing your resume...'):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

def display_score_meter(score: float):
    """Display an animated score meter."""
    st.markdown(
        f"""
        <div class="score-meter" style="text-align: center;">
            <div class="score-value" style="font-size: 48px; color: {'green' if score >= 70 else 'orange' if score >= 50 else 'red'};">
                {score}%
            </div>
            <div class="score-bar" style="
                background: linear-gradient(to right, 
                    {'#28a745' if score >= 70 else '#ffc107' if score >= 50 else '#dc3545'} {score}%, 
                    #e9ecef {score}%);
                height: 20px;
                border-radius: 10px;
                transition: all 1s ease-in-out;
            ">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_skill_radar(skills: Dict[str, float]):
    """Display skills in a radar chart."""
    # Using Plotly for interactive radar chart
    import plotly.graph_objects as go
    
    fig = go.Figure(data=go.Scatterpolar(
        r=list(skills.values()),
        theta=list(skills.keys()),
        fill='toself'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False
    )
    
    st.plotly_chart(fig)

def create_animated_timeline(experience_data: List[Dict]):
    """Create an animated timeline of work experience."""
    st.markdown("""
        <style>
        .timeline-item {
            padding: 10px;
            border-left: 2px solid #007bff;
            margin-left: 20px;
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    for item in experience_data:
        st.markdown(f"""
            <div class="timeline-item">
                <h4>{item['title']}</h4>
                <p>{item['company']} | {item['duration']}</p>
                <p>{item['description']}</p>
            </div>
        """, unsafe_allow_html=True)

def show_interview_tips_carousel():
    """Display interview tips in an animated carousel."""
    tips = [
        "Maintain eye contact with the camera 👀",
        "Speak clearly and at a moderate pace 🗣️",
        "Use the STAR method for behavioral questions ⭐",
        "Prepare relevant technical examples 💻",
        "Ask thoughtful questions at the end 🤔"
    ]
    
    tip_placeholder = st.empty()
    while True:
        for tip in tips:
            tip_placeholder.markdown(f"### 💡 Tip: {tip}")
            time.sleep(3)

# Add custom CSS for animations
def load_custom_css():
    st.markdown("""
        <style>
        /* Mumbai Indians theme colors */
        :root {
            --mi-blue: #004BA0;
            --mi-gold: #FFB700;
            --mi-dark-blue: #003670;
            --mi-light-blue: #0066CC;
        }

        /* Background */
        .stApp {
            background: #001733;
            background-image: linear-gradient(135deg, #001733 25%, #002147 100%);
        }

        /* Welcome section styling */
        .highlight-box {
            background: linear-gradient(135deg, var(--mi-blue), var(--mi-dark-blue));
            border: 2px solid var(--mi-gold);
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 40px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0, 75, 160, 0.3);
        }

        .highlight-box h2 {
            color: var(--mi-gold) !important;
            font-size: 2.5em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .highlight-box p {
            color: #ffffff !important;
            font-size: 1.2em;
        }

        /* Feature cards styling */
        .feature-card-new {
            background: linear-gradient(135deg, var(--mi-blue), var(--mi-dark-blue));
            padding: 30px;
            border-radius: 20px;
            margin: 15px 0;
            transition: all 0.3s ease;
            border: 2px solid var(--mi-gold);
            box-shadow: 0 5px 15px rgba(0, 75, 160, 0.2);
        }

        .feature-card-new:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(255, 183, 0, 0.3);
            border-color: #FFD700;
            background: linear-gradient(135deg, var(--mi-dark-blue), var(--mi-blue));
        }

        .feature-card-new .icon {
            font-size: 3em;
            margin-bottom: 20px;
            text-align: center;
            color: var(--mi-gold);
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .feature-card-new h3 {
            color: var(--mi-gold) !important;
            margin-bottom: 15px;
            font-size: 1.5em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .feature-card-new p {
            color: #ffffff !important;
            margin-bottom: 20px;
            font-size: 1.1em;
            line-height: 1.6;
        }

        .feature-card-new ul {
            list-style-type: none;
            padding-left: 0;
            margin-top: 20px;
        }

        .feature-card-new ul li {
            color: #ffffff;
            margin: 12px 0;
            padding-left: 25px;
            position: relative;
            font-size: 1.05em;
        }

        .feature-card-new ul li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: var(--mi-gold);
        }

        /* Practice section styling */
        .practice-section {
            background: linear-gradient(135deg, var(--mi-blue), var(--mi-dark-blue));
            padding: 40px;
            border-radius: 20px;
            margin: 30px 0;
            border: 2px solid var(--mi-gold);
            color: white;
        }

        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, var(--mi-gold), #FFD700);
            padding: 12px 30px;
            border-radius: 30px;
            border: none;
            color: var(--mi-dark-blue);
            font-weight: 700;
            font-size: 1.1em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 20px auto;
            display: block;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 183, 0, 0.3);
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 183, 0, 0.4);
            background: linear-gradient(135deg, #FFD700, var(--mi-gold));
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background: var(--mi-dark-blue);
            border-radius: 10px;
            color: var(--mi-gold);
            font-weight: 600;
            padding: 10px 25px;
            border: 2px solid var(--mi-gold);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: var(--mi-gold);
            color: var(--mi-dark-blue);
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: var(--mi-gold);
            color: var(--mi-dark-blue);
        }

        /* File uploader styling */
        .stFileUploader {
            padding: 20px;
            border-radius: 15px;
            border: 2px dashed var(--mi-gold);
            background: rgba(0, 75, 160, 0.2);
        }

        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--mi-gold), #FFD700);
        }

        /* Dark theme text colors */
        .stMarkdown {
            color: white !important;
        }
        
        h1, h2, h3, p {
            color: white !important;
        }

        /* Section card styling */
        .section-card {
            background: linear-gradient(135deg, var(--mi-blue), var(--mi-dark-blue));
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 2px solid var(--mi-gold);
            color: white;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            background: var(--mi-dark-blue);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--mi-gold);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #FFD700;
        }

        /* Glowing effects */
        .feature-card-new:hover .icon {
            animation: glow 1.5s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from {
                text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px var(--mi-gold);
            }
            to {
                text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px var(--mi-gold);
            }
        }

        /* Custom Image Container with Golden Border */
        .golden-frame {
            padding: 8px;
            border: 3px solid var(--mi-gold);
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(255, 183, 0, 0.2);
            background: linear-gradient(135deg, var(--mi-blue), var(--mi-dark-blue));
            transition: all 0.3s ease;
            display: block;
        }

        .golden-frame:hover {
            box-shadow: 0 0 30px rgba(255, 183, 0, 0.4);
            transform: translateY(-5px);
        }

        .golden-frame img {
            border-radius: 10px;
            width: 100%;
            height: auto;
            display: block;
        }
        </style>
    """, unsafe_allow_html=True) 
