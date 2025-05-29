"""
Prompt Templates for AI Cover Letter Generator

This module contains all prompt templates used in the AI Cover Letter Generator project.
These templates are used for:
1. Cover letter generation (with different tones)
2. Cover letter refinement based on feedback
3. Company research and information extraction
"""

# System prompts for different tones
COVER_LETTER_BASE_PROMPT = "You are an expert cover letter writer who crafts personalized and effective cover letters. Keep it informal and friendly."

TONE_PROMPTS = {
    "Enthusiastic": "Write with enthusiasm and passion that demonstrates excitement for the position.",
    "Confident": "Write with confidence and authority that emphasizes achievements and capabilities.",
    "Concise": "Write a brief but impactful cover letter that gets straight to the point."
}

# Human prompts for cover letter generation
COVER_LETTER_WITH_COMPANY_INFO_PROMPT = """
Please generate a cover letter for the job described below.

# Job Description:
{job_description}

# My Personal History/Resume:
{personal_history}

# Company Information (use this to personalize your letter):
{company_info}

Generate a well-structured cover letter that:
1. Begin with eye-catching start.
2. Highlights my relevant skills and experiences that match the job requirements
3. Explains why I'm a good fit for the role and the company
4. Shows my understanding of the company's values, mission, or recent achievements
5. Concludes with what I want to do with your company

The letter should be concise (less than 300 words), engaging, and tailored specifically to this job opportunity.
Use the company information to make the letter more personalized, but do not directly quote it.
"""

COVER_LETTER_WITHOUT_COMPANY_INFO_PROMPT = """
Please generate a cover letter for the job described below.

# Job Description:
{job_description}

# My Personal History/Resume:
{personal_history}

Generate a well-structured cover letter that:
1. Begin with eye-catching start. (Cut to the chase.)
2. Highlights my relevant skills and experiences that match the job requirements
3. Explains why I'm a good fit for the role and the company
4. Concludes with what I want to do with your company

The letter should be concise (less than 300 words), engaging, and tailored specifically to this job opportunity.
"""

# Human prompts for cover letter update with feedback
COVER_LETTER_UPDATE_WITH_COMPANY_INFO_PROMPT = """
I have a cover letter that I'd like to improve based on specific feedback.

# Original Job Description:
{job_description}

# My Personal History/Resume:
{personal_history}

# Company Information (use this to personalize your letter):
{company_info}

# Current Cover Letter:
{original_cover_letter}

# My Feedback for Improvement:
{feedback}

Please update the cover letter according to my feedback while maintaining:
1. The relevant match between my skills and the job requirements
2. A professional and engaging tone
3. A concise structure (still under 300 words)
4. The same overall format

Use the company information to make the letter more personalized, but do not directly quote it.
Return ONLY the complete updated cover letter without explanations or notes.
"""

COVER_LETTER_UPDATE_WITHOUT_COMPANY_INFO_PROMPT = """
I have a cover letter that I'd like to improve based on specific feedback.

# Original Job Description:
{job_description}

# My Personal History/Resume:
{personal_history}

# Current Cover Letter:
{original_cover_letter}

# My Feedback for Improvement:
{feedback}

Please update the cover letter according to my feedback while maintaining:
1. The relevant match between my skills and the job requirements
2. A professional and engaging tone
3. A concise structure (still under 300 words)
4. The same overall format

Return ONLY the complete updated cover letter without explanations or notes.
"""

# Company research agent prompts
COMPANY_RESEARCH_SYSTEM_PROMPT = """
You are a company research assistant specialized in extracting relevant information for job applications.
Your goal is to find accurate, useful information about companies that would help a job applicant customize their cover letter.

For each company, try to extract the following information:
1. Company overview and main business areas
2. Mission, vision, and values
3. Company culture and work environment
4. Recent news, achievements, or initiatives
5. Products or services they're known for

Be concise and factual. Only include information that would be useful for a cover letter.
Always cite your sources by mentioning where the information came from.
If you can't find specific information about something, acknowledge that and move on.
Focus on professional, business-relevant information and avoid gossip or unverified claims.

IMPORTANT: Present your findings in a structured format that clearly organizes the information.
"""

COMPANY_NAME_EXTRACTION_SYSTEM_PROMPT = """
You are an assistant that extracts company names from job descriptions. Return ONLY the company name, nothing else.
"""

COMPANY_NAME_EXTRACTION_HUMAN_PROMPT = """
Extract the company name from this job description:

{job_description}
"""

COMPANY_RESEARCH_HUMAN_PROMPT = """
Research the company: {company_name}. Extract information useful for a job application cover letter.
"""

def create_system_prompt_with_tone(tone):
    """
    Create a system prompt based on the specified tone.
    
    Args:
        tone (str): The desired tone for the cover letter
        
    Returns:
        str: The complete system prompt with the specified tone
    """
    if tone in TONE_PROMPTS:
        return f"{COVER_LETTER_BASE_PROMPT} {TONE_PROMPTS[tone]}"
    else:
        # For custom tone or any other tone not in the predefined list
        return f"{COVER_LETTER_BASE_PROMPT} Write in a {tone} tone that resonates with the employer."
