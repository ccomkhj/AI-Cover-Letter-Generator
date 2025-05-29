# AI Cover Letter Generator

Are you tired of creating cover letter for each job application?
This project is for you!

## Features

- **Advanced Multi-Agent Workflow** for comprehensive cover letter generation
- **RAG (Retrieval-Augmented Generation)** capabilities for company research
- **Intelligent Skill Extraction** to highlight your most relevant experiences
- Support for multiple LLM providers: OpenAI, Gemini, DeepSeek
- Interactive feedback system for refining cover letters
- Option to upload or paste job descriptions and personal history
- Generate cover letters as text or PDF files

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ccomkhj/AI-Cover-Letter-Generator
   cd AI-Cover-Letter-Generator
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys (optional):
   - Create a `.env` file in the project root directory
   - Add your API keys:

     ```env
     OPENAI_API_KEY=your_openai_api_key
     GOOGLE_API_KEY=your_google_api_key
     DEEPSEEK_API_KEY=your_deepseek_api_key
     ```

## Demo

![Cover Letter Generator Demo](/sample_data/demo.png)

## Usage

1. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to [http://localhost:8501](http://localhost:8501)

## How It Works

### Multi-Agent Workflow

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      AI Cover Letter Generator                          │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Step 1: Initial Setup                                                   │
│  - Configure LLM provider and model                                     │
│  - Process job description and personal history                         │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Step 2: Company Research Agent (RAG)                                    │
│  - Extract company name from job description                            │
│  - Search web for company information                                   │
│  - Synthesize relevant company details                                  │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Step 3: Initial Cover Letter Generation                                 │
│  - Generate personalized cover letter                                   │
│  - Incorporate company information                                      │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Step 4: Skills Analysis Agent                                           │
│  - Extract key skills from personal history                             │
│  - Identify missing skills in the cover letter                          │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Step 5: Cover Letter Enhancement                                        │
│  - Add missing relevant skills                                          │
│  - Refine based on job requirements                                     │
│  - Ensure appropriate tone and style                                    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Step 6: Feedback Loop (Optional)                                        │
│  - Process user feedback                                                │
│  - Further refine cover letter                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### RAG Implementation

The project leverages Retrieval-Augmented Generation (RAG) through the CompanyResearchAgent:

1. **Retrieval**: The agent uses DuckDuckGo Search (default) or Tavily Search (if API key provided) to retrieve relevant information about the company mentioned in the job description.

2. **Augmentation**: The retrieved information is processed and synthesized into a concise company profile.

3. **Generation**: The LLM uses this company information to create a more personalized and targeted cover letter that demonstrates knowledge of the company's values, products, and culture.

## Sample Data

The `sample_data` directory contains example files:

- `job_description.txt`: An example job posting for an AI/ML Software Engineer
- `personal_history.txt`: A sample resume and personal history

You can use these files to test the application without creating your own.
