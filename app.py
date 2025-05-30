import os
import streamlit as st
from dotenv import load_dotenv
from cover_letter_generator import CoverLetterGenerator
from pathlib import Path
from pdf_generator import generate_cover_letter_pdf

# Initialize session state variables if they don't exist
for key in ['cover_letter', 'original_job_description', 'original_personal_history', 
           'original_tone', 'provider', 'model', 'updated_cover_letter', 'feedback_text']:
    if key not in st.session_state:
        st.session_state[key] = ""
        
if 'enable_research' not in st.session_state:
    st.session_state['enable_research'] = True
        
if 'has_generated' not in st.session_state:
    st.session_state['has_generated'] = False
    
if 'update_success' not in st.session_state:
    st.session_state['update_success'] = False
    
if 'update_error' not in st.session_state:
    st.session_state['update_error'] = ""
    
# Additional session state variables for the agentic workflow
if 'generation_stage' not in st.session_state:
    st.session_state['generation_stage'] = "idle"  # idle, generating, analyzing, improving, done

# Function to update cover letter based on feedback
def update_cover_letter():
    # Get the feedback from the text area
    feedback = st.session_state.get('feedback_text', '')
    
    if feedback.strip():
        with st.spinner("Updating your cover letter..."):
            try:
                # Create generator instance with the same model as before
                generator = CoverLetterGenerator(
                    provider=st.session_state.get('provider', 'openai'),
                    model=st.session_state.get('model', 'gpt-3.5-turbo')
                )
                
                # Update cover letter based on feedback
                updated_letter = generator.update_with_feedback(
                    original_cover_letter=st.session_state.get('cover_letter', ''),
                    job_description=st.session_state.get('original_job_description', ''),
                    personal_history=st.session_state.get('original_personal_history', ''),
                    feedback=feedback,
                    tone=st.session_state.get('original_tone', 'Enthusiastic'),
                    research_company='enable_research' in st.session_state and st.session_state['enable_research']
                )
                
                # Print for debugging
                print(f"Updated letter length: {len(updated_letter)}")
                
                # Store the updated cover letter
                st.session_state['updated_cover_letter'] = updated_letter
                # Set a flag to indicate update was successful
                st.session_state['update_success'] = True
                
                # Force rerun to update the UI
                st.rerun()
            except Exception as e:
                st.session_state['update_error'] = f"Error updating cover letter: {str(e)}"
                print(f"Error in update_cover_letter: {str(e)}")
    else:
        # Set error message in session state
        st.session_state['update_error'] = "Please provide feedback to update your cover letter"

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
            
        # Web search API keys for company research
        st.header("Company Research Configuration")
        enable_research = st.checkbox("Enable Company Research", value=st.session_state['enable_research'], 
                                    help="Automatically research company information from the web to personalize your cover letter")
        st.session_state['enable_research'] = enable_research
        
        with st.expander("Search API Keys (Optional)"):
            tavily_api_key = st.text_input("Tavily API Key (Optional)", type="password",
                                        value=os.getenv("TAVILY_API_KEY", ""),
                                        help="Tavily provides more accurate search results. Get a free key at tavily.com")
            os.environ["TAVILY_API_KEY"] = tavily_api_key
        
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
                # Start the agentic workflow for cover letter generation
                st.session_state['generation_stage'] = "generating"
                
                # Create a placeholder for the progress messages
                progress_placeholder = st.empty()
                
                # Step 1: Initial setup
                progress_placeholder.info("Step 1/4: Setting up the cover letter generator...")
                
                # Create generator instance
                generator = CoverLetterGenerator(
                    provider=model_provider.lower().replace(" ", "_"),
                    model=model_name
                )
                
                # Set tone
                selected_tone = custom_tone if tone == "Custom" else tone
                
                # Generate cover letter with the agentic workflow
                with st.spinner("Generating your personalized cover letter..."):
                    # Step 2: Research company and generate initial letter
                    progress_placeholder.info("Step 2/4: Generating initial cover letter...")
                    
                    # Research company information if enabled
                    company_info = ""
                    if enable_research:
                        company_info = generator._research_company_info(job_description)
                    
                    # Generate initial cover letter
                    initial_letter = generator._initial_generation(job_description, personal_history, selected_tone, company_info)
                    
                    # Step 3: Analyze for missing information
                    progress_placeholder.info("Step 3/4: Analyzing for missing information...")
                    
                    # Extract key skills from personal history
                    skills_list = generator._extract_key_skills_from_personal_history(personal_history)
                    
                    # Identify missing skills in the cover letter
                    missing_skills = generator._identify_missing_skills(initial_letter, skills_list)
                    
                    # Step 4: Improve the cover letter
                    progress_placeholder.info("Step 4/4: Enhancing your cover letter...")
                    
                    # Self-improvement to address missing skills and add company information
                    cover_letter = generator._self_improvement(initial_letter, job_description, personal_history, selected_tone, missing_skills, company_info)
                
                # Update completion message
                progress_placeholder.success("✅ Cover letter generation complete! Agentic workflow successfully enhanced your letter.")
                
                # Store the generated cover letter in session state
                st.session_state['cover_letter'] = cover_letter
                st.session_state['original_job_description'] = job_description
                st.session_state['original_personal_history'] = personal_history
                st.session_state['original_tone'] = selected_tone
                st.session_state['provider'] = model_provider.lower().replace(" ", "_")
                st.session_state['model'] = model_name
                st.session_state['has_generated'] = True  # Flag to track if a letter has been generated
                st.session_state['generation_stage'] = "done"
                
                # Clear any previously updated letter
                st.session_state['updated_cover_letter'] = ""
                
                # Download options
                col1_download, col2_download = st.columns(2)
                
                with col1_download:
                    # Text download option
                    st.download_button(
                        label="Download as Text",
                        data=cover_letter,
                        file_name="cover_letter.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key="download_original_text_generation"
                    )
                
                with col2_download:
                    # PDF download option with nice formatting
                    pdf_buffer = generate_cover_letter_pdf(cover_letter)
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_buffer,
                        file_name="cover_letter.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_original_pdf_generation"
                    )
                        
        # Display the cover letter(s)
        if st.session_state.get('has_generated', False):
            st.subheader("Your Cover Letter")
            
            # Always show the original cover letter
            st.markdown("### Original Cover Letter")
            st.text_area("Original", value=st.session_state['cover_letter'], height=300, key="display_original")
            
            # Download options for original cover letter
            col1_download, col2_download = st.columns(2)
            
            with col1_download:
                # Text download option
                st.download_button(
                    label="Download Original as Text",
                    data=st.session_state['cover_letter'],
                    file_name="original_cover_letter.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_original_text_display"
                )
            
            with col2_download:
                # PDF download option with nice formatting
                pdf_buffer = generate_cover_letter_pdf(st.session_state['cover_letter'])
                st.download_button(
                    label="Download Original as PDF",
                    data=pdf_buffer,
                    file_name="original_cover_letter.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_original_pdf_display"
                )
            
            # If there's an updated version, show it too
            if st.session_state.get('updated_cover_letter', ""):
                st.markdown("### Updated Cover Letter")
                st.text_area("Updated", value=st.session_state['updated_cover_letter'], height=300, key="display_updated")
                
                # Download options for updated cover letter
                col1_updated, col2_updated = st.columns(2)
                
                with col1_updated:
                    # Text download option
                    st.download_button(
                        label="Download Updated as Text",
                        data=st.session_state['updated_cover_letter'],
                        file_name="updated_cover_letter.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key="download_updated_text_display"
                    )
                
                with col2_updated:
                    # PDF download option with nice formatting
                    pdf_buffer = generate_cover_letter_pdf(st.session_state['updated_cover_letter'])
                    st.download_button(
                        label="Download Updated as PDF",
                        data=pdf_buffer,
                        file_name="updated_cover_letter.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_updated_pdf_display"
                    )
            
            # Feedback section for refinement
            st.subheader("Refine Your Cover Letter")
            st.write("Not satisfied? Provide feedback to update your cover letter.")
            st.info("""Your cover letter has already been enhanced through our agentic workflow, which:
1. Generated an initial cover letter based on your inputs
2. Identified and added missing skills from your personal history
3. Incorporated relevant company information (if enabled)

Any feedback you provide will further refine this already-enhanced letter.""")
            
            # Display success message if update was successful
            if st.session_state.get('update_success', False):
                st.success("✅ Cover letter updated successfully!")
                # Reset the flag
                st.session_state['update_success'] = False
                
            # Display error message if there was an error
            if st.session_state.get('update_error', ""):
                st.error(st.session_state['update_error'])
                # Reset the error message
                st.session_state['update_error'] = ""
                
            # Use session state for the feedback text area
            st.text_area(
                "What would you like to change or improve?",
                placeholder="For example: 'Make it more concise', 'Add more details about my Python skills', 'Focus more on leadership experience'...",
                height=100,
                key="feedback_text"
            )
            
            # Create a button that calls the update function directly
            if st.button("Update Cover Letter", use_container_width=True, key="update_button"):
                if st.session_state.get('feedback_text', "").strip():
                    # Create a placeholder for the update progress
                    update_progress = st.empty()
                    update_progress.info("Updating your cover letter based on feedback...")
                    
                    # Call the update function
                    update_cover_letter()
                    
                    # Clear the progress message (success message is shown in update_cover_letter function)
                    update_progress.empty()
                else:
                    st.warning("Please provide feedback to update your cover letter")

if __name__ == "__main__":
    main()
