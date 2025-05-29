from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from langchain.schema.output_parser import StrOutputParser

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
        base_prompt = "You are an expert cover letter writer who crafts personalized and effective cover letters. Keep it informal and friendly."
        
        tone_prompts = {
            "Enthusiastic": "Write with enthusiasm and passion that demonstrates excitement for the position.",
            "Confident": "Write with confidence and authority that emphasizes achievements and capabilities.",
            "Concise": "Write a brief but impactful cover letter that gets straight to the point."
        }
        
        if tone in tone_prompts:
            return f"{base_prompt} {tone_prompts[tone]}"
        else:
            # For custom tone or any other tone not in the predefined list
            return f"{base_prompt} Write in a {tone} tone that resonates with the employer."
    
    def generate(self, job_description, personal_history, tone="Enthusiastic"):
        """
        Generate a cover letter based on the job description and personal history.
        
        Args:
            job_description (str): The job description text
            personal_history (str): The applicant's personal history/resume text
            tone (str): The desired tone for the cover letter
            
        Returns:
            str: The generated cover letter
        """
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._create_system_prompt(tone)),
            ("human", """
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
            """)
        ])
        
        # Create the chain
        chain = prompt | self.llm | StrOutputParser()
        
        # Generate the cover letter
        return chain.invoke({
            "job_description": job_description,
            "personal_history": personal_history
        })
