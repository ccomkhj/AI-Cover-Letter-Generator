"""
Company Research Agent using LangChain

This module provides functionality to research companies using web search 
and extract relevant information for cover letter generation.
"""
import re
from typing import Dict, List, Optional, Any

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
import prompt

# Create our own DuckDuckGo search run function since the import path has changed
class DuckDuckGoSearchRun:
    """Tool that adds a wrapper around DuckDuckGo Search."""
    
    def __init__(self, api_wrapper=None):
        self.api_wrapper = api_wrapper or DuckDuckGoSearchAPIWrapper()
        
    def run(self, query: str) -> str:
        """Run query through DuckDuckGo and parse result."""
        return self.api_wrapper.run(query)

class CompanyResearchAgent:
    """
    An agent that researches company information using web search tools.
    Uses LangChain's agent framework to perform intelligent searches and
    extract relevant information about companies.
    """
    
    def __init__(self, provider="openai", model="gpt-3.5-turbo"):
        """
        Initialize the company research agent.
        
        Args:
            provider (str): The LLM provider to use ('openai', 'google_gemini', 'deepseek')
            model (str): The model name to use
        """
        self.provider = provider
        self.model = model
        
        # Initialize the LLM (reusing code from CoverLetterGenerator)
        from cover_letter_generator import CoverLetterGenerator
        generator = CoverLetterGenerator(provider=provider, model=model)
        self.llm = generator.llm
        
        # Initialize search tools
        self.search_tools = self._initialize_search_tools()
        
        # Create the agent executor
        self.agent_executor = self._create_agent_executor()
    
    def _initialize_search_tools(self) -> List[Tool]:
        """Initialize the search tools for the agent."""
        # Use DuckDuckGo as the default search tool since it doesn't require an API key
        duckduckgo_search = DuckDuckGoSearchRun(
            api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=5)
        )
        
        search_tool = Tool(
            name="web_search",
            description="Search the web for information about a company. Input should be a search query.",
            func=duckduckgo_search.run
        )
        
        # Try to initialize Tavily search if API key is available
        try:
            import os
            if os.getenv("TAVILY_API_KEY"):
                tavily_search = TavilySearchResults(max_results=3)
                tavily_tool = Tool(
                    name="tavily_search",
                    description="Search the web for recent and factual information about a company. Input should be a search query.",
                    func=tavily_search.invoke
                )
                return [search_tool, tavily_tool]
        except (ImportError, Exception):
            pass
            
        return [search_tool]
    
    def _create_agent_executor(self) -> AgentExecutor:
        """Create the agent executor with the appropriate tools and prompt."""
        # Define the system prompt for the agent
        system_prompt = prompt.COMPANY_RESEARCH_SYSTEM_PROMPT
        
        # Create the agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Create the agent using the LLM and tools
        agent = create_tool_calling_agent(self.llm, self.search_tools, prompt)
        
        # Create the agent executor
        return AgentExecutor(agent=agent, tools=self.search_tools, verbose=True)
    
    def extract_company_name(self, job_description: str) -> Optional[str]:
        """
        Extract the company name from a job description.
        
        Args:
            job_description (str): The job description text
            
        Returns:
            Optional[str]: The extracted company name or None if not found
        """
        # First, try to find direct mentions of company name
        company_patterns = [
            r"Company:?\s*([A-Z][A-Za-z0-9\s&,.-]+)(?:\n|\.|\()",
            r"About\s+([A-Z][A-Za-z0-9\s&,.-]+)(?:\n|\.|\:)",
            r"([A-Z][A-Za-z0-9\s&,.-]+)\s+is\s+(?:a|an)\s+(?:leading|innovative|growing)",
            r"Job\s+at\s+([A-Z][A-Za-z0-9\s&,.-]+)",
            r"Join\s+(?:the\s+)?(?:team\s+at\s+)?([A-Z][A-Za-z0-9\s&,.-]+)",
            r"Welcome\s+to\s+([A-Z][A-Za-z0-9\s&,.-]+)"
        ]
        
        for pattern in company_patterns:
            matches = re.search(pattern, job_description)
            if matches:
                company_name = matches.group(1).strip()
                return company_name
        
        # If direct extraction fails, ask the LLM to identify the company
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", prompt.COMPANY_NAME_EXTRACTION_SYSTEM_PROMPT),
                ("human", prompt.COMPANY_NAME_EXTRACTION_HUMAN_PROMPT.format(job_description=job_description[:1000]))
            ])
            
            chain = prompt | self.llm
            result = chain.invoke({})
            if isinstance(result, str) and len(result) > 0 and len(result) < 100:
                return result.strip()
            return None
        except Exception:
            return None
    
    def research_company(self, company_name: str = None, job_description: str = None) -> Dict[str, Any]:
        """
        Research a company using web search and extract relevant information.
        
        Args:
            company_name (str, optional): The name of the company to research
            job_description (str, optional): A job description from which to extract company info
            
        Returns:
            Dict[str, Any]: Dictionary containing the research results
        """
        # Extract company name from job description if not provided
        if company_name is None and job_description is not None:
            company_name = self.extract_company_name(job_description)
            
        if not company_name:
            return {
                "success": False,
                "error": "Could not identify company name",
                "company_info": None
            }
        
        # Run the agent to research the company
        try:
            result = self.agent_executor.invoke({
                "input": prompt.COMPANY_RESEARCH_HUMAN_PROMPT.format(company_name=company_name)
            })
            
            return {
                "success": True,
                "company_name": company_name,
                "company_info": result.get("output", ""),
                "sources": result.get("intermediate_steps", [])
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "company_name": company_name,
                "company_info": None
            }


if __name__ == "__main__":
    # Example usage
    agent = CompanyResearchAgent()
    company_info = agent.research_company(company_name="Microsoft")
    print(company_info.get("company_info", "No information found"))
