from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from langchain.schema.output_parser import StrOutputParser
from company_research_agent import CompanyResearchAgent
import prompt

class CoverLetterGenerator:
    """
    A class to generate cover letters using different LLM providers through LangChain.
    Supports OpenAI, Google Gemini, and DeepSeek.
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
    
    def generate(self, job_description, personal_history, tone="Enthusiastic", research_company=True):
        """
        Generate a cover letter based on the job description and personal history.
        
        Args:
            job_description (str): The job description text
            personal_history (str): The applicant's personal history/resume text
            tone (str): The desired tone for the cover letter
            research_company (bool): Whether to research company information
            
        Returns:
            str: The generated cover letter
        """
        # Research company information if enabled
        company_info = ""
        if research_company:
            try:
                # Create company research agent with the same LLM settings
                research_agent = CompanyResearchAgent(provider=self.provider, model=self.model)
                
                # Research the company based on the job description
                research_results = research_agent.research_company(job_description=job_description)
                
                if research_results.get("success", False):
                    company_info = research_results.get("company_info", "")
            except Exception as e:
                print(f"Error researching company: {str(e)}")
        
        # Create the prompt template with company information if available
        if company_info:
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self._create_system_prompt(tone)),
                ("human", prompt.COVER_LETTER_WITH_COMPANY_INFO_PROMPT)
            ])
            
            # Create the chain
            chain = prompt | self.llm | StrOutputParser()
            
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
        if research_company and "company information" in feedback.lower():
            try:
                # Create company research agent with the same LLM settings
                research_agent = CompanyResearchAgent(provider=self.provider, model=self.model)
                
                # Research the company based on the job description
                research_results = research_agent.research_company(job_description=job_description)
                
                if research_results.get("success", False):
                    company_info = research_results.get("company_info", "")
            except Exception as e:
                print(f"Error researching company: {str(e)}")
        
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
