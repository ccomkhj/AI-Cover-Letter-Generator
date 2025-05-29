from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from langchain.schema.output_parser import StrOutputParser
from company_research_agent import CompanyResearchAgent
import prompt
import re

class CoverLetterGenerator:
    """
    A class to generate cover letters using different LLM providers through LangChain.
    Supports OpenAI, Google Gemini, and DeepSeek.
    
    Implements an agentic workflow:
    1. Initial generation of cover letter
    2. Self-improvement by checking for missing information
    3. Further updates based on user feedback
    """
    
    def __init__(self, provider="openai", model="gpt-3.5-turbo"):
        """
        Initialize the cover letter generator with the specified provider and model.
        
        Args:
            provider (str): The LLM provider to use ('openai', 'google_gemini', 'deepseek')
            model (str): The model name to use
        """
        self.provider = provider
        self.model = model
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on the provider."""
        if self.provider == "openai":
            return ChatOpenAI(model_name=self.model)
        elif self.provider == "google_gemini":
            return ChatGoogleGenerativeAI(model=self.model)
        elif self.provider == "deepseek":
            return ChatDeepSeek(model_name=self.model)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _create_system_prompt(self, tone):
        """Create a system prompt based on the specified tone."""
        return prompt.create_system_prompt_with_tone(tone)
    
    def _extract_key_skills_from_personal_history(self, personal_history):
        """
        Extract key skills and experiences from the personal history.
        
        Args:
            personal_history (str): The personal history text
            
        Returns:
            list: A list of key skills and experiences
        """
        # Create a prompt to extract key skills
        extract_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt.SKILLS_EXTRACTION_SYSTEM_PROMPT),
            ("human", prompt.SKILLS_EXTRACTION_HUMAN_PROMPT)
        ])
        
        # Create the chain
        extract_chain = extract_prompt | self.llm | StrOutputParser()
        
        # Extract key skills
        extracted_skills = extract_chain.invoke({
            "personal_history": personal_history
        })
        
        # Convert the extracted skills to a list
        skills_list = [skill.strip() for skill in re.split(r'\n|\d+\.', extracted_skills) if skill.strip()]
        return skills_list
    
    def _identify_missing_skills(self, cover_letter, skills_list):
        """
        Identify key skills from personal history that are missing in the cover letter.
        
        Args:
            cover_letter (str): The generated cover letter
            skills_list (list): List of key skills from personal history
            
        Returns:
            list: A list of missing skills
        """
        # Create a prompt to identify missing skills
        missing_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt.MISSING_SKILLS_SYSTEM_PROMPT),
            ("human", prompt.MISSING_SKILLS_HUMAN_PROMPT)
        ])
        
        # Create the chain
        missing_chain = missing_prompt | self.llm | StrOutputParser()
        
        # Identify missing skills
        missing_skills_text = missing_chain.invoke({
            "cover_letter": cover_letter,
            "skills": "\n".join([f"- {skill}" for skill in skills_list])
        })
        
        # Convert the missing skills to a list
        missing_skills = [skill.strip() for skill in re.split(r'\n|\d+\.|-', missing_skills_text) if skill.strip()]
        return missing_skills
    
    def _research_company_info(self, job_description):
        """
        Research company information based on job description.
        
        Args:
            job_description (str): The job description text
            
        Returns:
            str: Company information if found, empty string otherwise
        """
        company_info = ""
        try:
            # Create company research agent with the same LLM settings
            research_agent = CompanyResearchAgent(provider=self.provider, model=self.model)
            
            # Research the company based on the job description
            research_results = research_agent.research_company(job_description=job_description)
            
            if research_results.get("success", False):
                company_info = research_results.get("company_info", "")
        except Exception as e:
            print(f"Error researching company: {str(e)}")
            
        return company_info
    
    def _initial_generation(self, job_description, personal_history, tone, company_info=""):
        """
        Generate the initial cover letter.
        
        Args:
            job_description (str): The job description text
            personal_history (str): The applicant's personal history/resume text
            tone (str): The desired tone for the cover letter
            company_info (str): Company information if available
            
        Returns:
            str: The initially generated cover letter
        """
        if company_info:
            # Create the prompt template with company information
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self._create_system_prompt(tone)),
                ("human", prompt.COVER_LETTER_WITH_COMPANY_INFO_PROMPT)
            ])
            
            # Create the chain
            chain = prompt_template | self.llm | StrOutputParser()
            
            # Generate the cover letter with company information
            return chain.invoke({
                "job_description": job_description,
                "personal_history": personal_history,
                "company_info": company_info
            })
        else:
            # Create the prompt template without company information
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self._create_system_prompt(tone)),
                ("human", prompt.COVER_LETTER_WITHOUT_COMPANY_INFO_PROMPT)
            ])
            
            # Create the chain
            chain = prompt_template | self.llm | StrOutputParser()
            
            # Generate the cover letter
            return chain.invoke({
                "job_description": job_description,
                "personal_history": personal_history
            })
    
    def _self_improvement(self, initial_letter, job_description, personal_history, tone, missing_skills, company_info=""):
        """
        Improve the cover letter by addressing missing skills and company information.
        
        Args:
            initial_letter (str): The initially generated cover letter
            job_description (str): The job description text
            personal_history (str): The applicant's personal history/resume text
            tone (str): The desired tone for the cover letter
            missing_skills (list): List of missing skills to incorporate
            company_info (str): Company information if available
            
        Returns:
            str: The improved cover letter
        """
        # If no missing skills and no company info to add, return the initial letter
        if not missing_skills and not company_info:
            return initial_letter
        
        # Create the self-improvement prompt
        if company_info:
            improve_prompt = ChatPromptTemplate.from_messages([
                ("system", self._create_system_prompt(tone) + " You are improving a cover letter by adding missing information."),
                ("human", prompt.SELF_IMPROVEMENT_WITH_COMPANY_INFO_PROMPT)
            ])
            
            # Create the chain
            improve_chain = improve_prompt | self.llm | StrOutputParser()
            
            # Generate the improved cover letter
            return improve_chain.invoke({
                "original_cover_letter": initial_letter,
                "job_description": job_description,
                "personal_history": personal_history,
                "missing_skills": "\n".join([f"- {skill}" for skill in missing_skills]) if missing_skills else "No missing skills",
                "company_info": company_info
            })
        else:
            improve_prompt = ChatPromptTemplate.from_messages([
                ("system", self._create_system_prompt(tone) + " You are improving a cover letter by adding missing information."),
                ("human", prompt.SELF_IMPROVEMENT_WITHOUT_COMPANY_INFO_PROMPT)
            ])
            
            # Create the chain
            improve_chain = improve_prompt | self.llm | StrOutputParser()
            
            # Generate the improved cover letter
            return improve_chain.invoke({
                "original_cover_letter": initial_letter,
                "job_description": job_description,
                "personal_history": personal_history,
                "missing_skills": "\n".join([f"- {skill}" for skill in missing_skills]) if missing_skills else "No missing skills"
            })
    
    def generate(self, job_description, personal_history, tone="Enthusiastic", research_company=True):
        """
        Generate a cover letter based on the job description and personal history using the agentic workflow.
        
        Workflow:
        1. Initial generation of cover letter
        2. Self-improvement by checking for missing information from personal history
        3. If company research is enabled, incorporate company information
        
        Args:
            job_description (str): The job description text
            personal_history (str): The applicant's personal history/resume text
            tone (str): The desired tone for the cover letter
            research_company (bool): Whether to research company information
            
        Returns:
            str: The generated cover letter
        """
        # Step 1: Research company information if enabled
        company_info = ""
        if research_company:
            company_info = self._research_company_info(job_description)
        
        # Step 2: Generate initial cover letter
        initial_letter = self._initial_generation(job_description, personal_history, tone, company_info)
        
        # Step 3: Extract key skills from personal history
        skills_list = self._extract_key_skills_from_personal_history(personal_history)
        
        # Step 4: Identify missing skills in the cover letter
        missing_skills = self._identify_missing_skills(initial_letter, skills_list)
        
        # Step 5: Self-improvement to address missing skills and add company information
        improved_letter = self._self_improvement(initial_letter, job_description, personal_history, tone, missing_skills, company_info)
        
        return improved_letter
        
    def update_with_feedback(self, original_cover_letter, job_description, personal_history, feedback, tone="Enthusiastic", research_company=True):
        """
        Update an existing cover letter based on user feedback.
        
        Args:
            original_cover_letter (str): The previously generated cover letter
            job_description (str): The original job description text
            personal_history (str): The original personal history/resume text
            feedback (str): User feedback on how to improve the cover letter
            tone (str): The desired tone for the cover letter
            research_company (bool): Whether to research company information
            
        Returns:
            str: The updated cover letter
        """
        # Research company information if enabled and not already in feedback
        company_info = ""
        if research_company and ("company information" in feedback.lower() or "company info" in feedback.lower()):
            company_info = self._research_company_info(job_description)
        
        # Create the prompt template for updating with feedback, including company info if available
        if company_info:
            update_prompt = ChatPromptTemplate.from_messages([
                ("system", self._create_system_prompt(tone) + " You are refining an existing cover letter based on specific feedback."),
                ("human", prompt.COVER_LETTER_UPDATE_WITH_COMPANY_INFO_PROMPT)
            ])
            
            # Create the chain
            update_chain = update_prompt | self.llm | StrOutputParser()
            
            # Generate the updated cover letter with company information
            return update_chain.invoke({
                "original_cover_letter": original_cover_letter,
                "job_description": job_description,
                "personal_history": personal_history,
                "feedback": feedback,
                "company_info": company_info
            })
        else:
            # Create the prompt template without company information
            update_prompt = ChatPromptTemplate.from_messages([
                ("system", self._create_system_prompt(tone) + " You are refining an existing cover letter based on specific feedback."),
                ("human", prompt.COVER_LETTER_UPDATE_WITHOUT_COMPANY_INFO_PROMPT)
            ])
            
            # Create the chain
            update_chain = update_prompt | self.llm | StrOutputParser()
            
            # Generate the updated cover letter
            return update_chain.invoke({
                "original_cover_letter": original_cover_letter,
                "job_description": job_description,
                "personal_history": personal_history,
                "feedback": feedback
            })
