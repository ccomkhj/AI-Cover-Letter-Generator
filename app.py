import os
import streamlit as st
from dotenv import load_dotenv
from cover_letter_generator import CoverLetterGenerator
from pathlib import Path
from pdf_generator import generate_cover_letter_pdf

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon="📝",
    layout="wide"
)

def main():
    st.title("AI Cover Letter Generator")
    st.write("Generate customized cover letters using your job description and personal history")
    
    # Sidebar for model selection and configuration
    with st.sidebar:
        st.header("Model Configuration")
        model_provider = st.selectbox(
            "Select Model Provider",
            options=["OpenAI", "Google Gemini", "DeepSeek"]
        )
        
        # API Key inputs
        if model_provider == "OpenAI":
            api_key = st.text_input("OpenAI API Key", type="password", 
                                    value=os.getenv("OPENAI_API_KEY", ""))
            os.environ["OPENAI_API_KEY"] = api_key
            model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"])
        
        elif model_provider == "Google Gemini":
            api_key = st.text_input("Google API Key", type="password", 
                                    value=os.getenv("GOOGLE_API_KEY", ""))
            os.environ["GOOGLE_API_KEY"] = api_key
            model_name = st.selectbox("Model", ["gemini-2.5-flash-preview-04-17"])
        
        elif model_provider == "DeepSeek":
            api_key = st.text_input("DeepSeek API Key", type="password", 
                                    value=os.getenv("DEEPSEEK_API_KEY", ""))
            os.environ["DEEPSEEK_API_KEY"] = api_key
            model_name = "deepseek-chat"
        
        st.header("Tone Configuration")
        tone = st.selectbox(
            "Select Tone",
            options=["Enthusiastic", "Confident", "Concise", "Custom"]
        )
        
        if tone == "Custom":
            custom_tone = st.text_area("Describe your preferred tone")
        else:
            custom_tone = None

    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Job Description")
        job_description_source = st.radio(
            "Job Description Source",
            options=["Upload File", "Paste Text"],
            horizontal=True
        )
        
        if job_description_source == "Upload File":
            job_file = st.file_uploader("Upload Job Description", type=["txt", "pdf"])
            if job_file:
                job_description = job_file.getvalue().decode()
            else:
                job_description = ""
        else:
            job_description = st.text_area(
                "Paste Job Description", 
                height=300,
                placeholder="Paste the job description here..."
            )
            
        # Check if job description is empty
        if not job_description.strip():
            # Load default job description from sample data
            sample_path = Path("sample_data/job_description.txt")
            if sample_path.exists():
                with open(sample_path, "r") as f:
                    job_description = f.read()
                st.warning("Using default job description from sample data. Upload or paste a specific job for a more relevant cover letter.")
        
        st.subheader("Personal History")
        personal_history_source = st.radio(
            "Personal History Source",
            options=["Upload File", "Paste Text"],
            horizontal=True
        )
        
        if personal_history_source == "Upload File":
            personal_file = st.file_uploader("Upload Personal History", type=["txt", "pdf"])
            if personal_file:
                personal_history = personal_file.getvalue().decode()
            else:
                personal_history = ""
        else:
            personal_history = st.text_area(
                "Paste Personal History", 
                height=300,
                placeholder="Paste your resume, skills, and relevant experience here..."
            )
            
        # Check if personal history is empty
        if not personal_history.strip():
            # Load default personal history from sample data
            sample_path = Path("sample_data/personal_history.txt")
            if sample_path.exists():
                with open(sample_path, "r") as f:
                    personal_history = f.read()
                st.warning("Using default personal history from sample data. Upload or paste your own for a more personalized cover letter.")

    with col2:
        st.subheader("Generated Cover Letter")
        
        if st.button("Generate Cover Letter", type="primary", use_container_width=True):
            if not job_description:
                st.error("Please provide a job description")
            else:
                with st.spinner("Generating your cover letter..."):
                    # Create generator instance
                    generator = CoverLetterGenerator(
                        provider=model_provider.lower().replace(" ", "_"),
                        model=model_name
                    )
                    
                    # Set tone
                    selected_tone = custom_tone if tone == "Custom" else tone
                    
                    # Generate cover letter
                    cover_letter = generator.generate(
                        job_description=job_description,
                        personal_history=personal_history,
                        tone=selected_tone
                    )
                    
                    st.text_area("Your Cover Letter", value=cover_letter, height=500)
                    
                    # Download options
                    col1_download, col2_download = st.columns(2)
                    
                    with col1_download:
                        # Text download option
                        st.download_button(
                            label="Download as Text",
                            data=cover_letter,
                            file_name="cover_letter.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col2_download:
                        # PDF download option with nice formatting
                        pdf_buffer = generate_cover_letter_pdf(cover_letter)
                        st.download_button(
                            label="Download as PDF",
                            data=pdf_buffer,
                            file_name="cover_letter.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

if __name__ == "__main__":
    main()
