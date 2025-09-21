import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# Set the page configuration
st.set_page_config(
    page_title="Pathfinder AI: Career Advisor", 
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for styling - Dark Professional Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header {
        background: linear-gradient(135deg, #e94560 0%, #f27121 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 20px 40px rgba(233, 69, 96, 0.4);
    }
    
    .main-header h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.3rem !important;
        opacity: 0.9;
        margin-bottom: 0 !important;
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.08);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(233, 69, 96, 0.3);
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .input-container h3 {
        color: #e94560 !important;
    }
    
    .input-container p {
        color: #ffffff !important;
        opacity: 0.8;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #f27121) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 15px 35px rgba(233, 69, 96, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 25px 50px rgba(233, 69, 96, 0.6) !important;
    }
    
    .response-container {
        background: rgba(255, 255, 255, 0.08);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid rgba(233, 69, 96, 0.3);
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
        color: white;
    }
    
    .response-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #e94560, #f27121);
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 15px !important;
        border: 2px solid rgba(233, 69, 96, 0.3) !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #e94560 !important;
        box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.2) !important;
    }
    
    /* Override Streamlit's default text colors */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.8s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Configure the Gemini AI API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    api_configured = True
    model = genai.GenerativeModel('gemini-2.5-pro')
except KeyError:
    api_configured = False

# Main header
st.markdown("""
<div class="main-header fade-in">
    <h1>🎯 Pathfinder AI: Your Personalized Career Guide</h1>
    <p>Discover the ideal career path for you and the skills you need to succeed using AI-powered insights</p>
</div>
""", unsafe_allow_html=True)

# Main input section
st.markdown("""
<div class="input-container fade-in">
    <h3 style="color: #e94560; margin-bottom: 1rem; text-align: center;">Tell Us About Yourself</h3>
    <p style="color: #ffffff; text-align: center; margin-bottom: 1.5rem; opacity: 0.8;">
        Share your interests, favorite subjects, hobbies, and what excites you most about your future career
    </p>
</div>
""", unsafe_allow_html=True)

# Input area
interests_input = st.text_area(
    "Your Interests & Background:",
    placeholder="""Example: I love solving math problems, enjoy playing video games, and I'm interested in how technology works.""",
    height=120,
    help="Be as detailed as possible - mention your education, experience, interests, and career goals."
)

# Generate button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button(
        "🚀 Generate My Career Path", 
        help="Click to get AI-powered career recommendations"
    )

# AI generation logic
if generate_button:
    if not api_configured:
        st.error("🔑 **API Configuration Required**")
        st.markdown("""
        Please add your Google API key to `.streamlit/secrets.toml`:
        ```toml
        GOOGLE_API_KEY = "your_api_key_here"
        ```
        """)
        st.stop()
    
    if interests_input:
        with st.spinner("🤖 AI is analyzing your profile and generating personalized career recommendations..."):
            # Progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            progress_bar.empty()
            
            # AI prompt
            prompt = f"""
            You are an expert career advisor specializing in career guidance. 

            A person has provided: "{interests_input}"

            Please provide career guidance using this format:

            ## 🎯 Recommended Career Paths
            
            ### Career Path 1: [Career Title]
            **Why this fits you:** [Brief explanation]
            
            **Hard Skills Required:**
            • [Skill 1 with brief description]
            • [Skill 2 with brief description] 
            • [Skill 3 with brief description]
            
            **Soft Skills Required:**
            • [Skill 1 with brief description]
            • [Skill 2 with brief description]
            • [Skill 3 with brief description]
            
            **Actionable Steps:**
            1. **[Step Title]:** [Detailed actionable step]
            2. **[Step Title]:** [Detailed actionable step]
            3. **[Step Title]:** [Detailed actionable step]
            
            ### Career Path 2: [Career Title]
            [Same format as above]
            
            ## 💡 Additional Recommendations
            • [Industry insights]
            • [Networking suggestions]
            • [Career growth advice]
            """
            
            try:
                response = model.generate_content(prompt)
                
                # Display response
                st.markdown("""
                <div class="response-container fade-in">
                    <h2 style="color: #e94560; text-align: center; margin-bottom: 2rem;">
                        🎉 Your Personalized Career Roadmap
                    </h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(response.text)
                st.success("✨ **Career recommendations generated successfully!**")
                
            except Exception as e:
                st.error(f"🚨 **AI Generation Error:** {e}")
    else:
        st.warning("✍️ **Please tell us about your interests to get started!**")
       