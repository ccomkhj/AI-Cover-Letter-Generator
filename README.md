# AI Cover Letter Generator

Are you tired of creating cover letter for each job application?
This project is for you!

## Features

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

## Sample Data

The `sample_data` directory contains example files:

- `job_description.txt`: An example job posting for an AI/ML Software Engineer
- `personal_history.txt`: A sample resume and personal history

You can use these files to test the application without creating your own.
