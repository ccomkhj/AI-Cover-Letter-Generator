# AI Cover Letter Generator

A LangChain-based application that uses multiple LLM providers (OpenAI, Google Gemini, DeepSeek) to generate customized cover letters based on job descriptions and personal history.

## Features

- Support for multiple LLM providers:
  - OpenAI (GPT-3.5 Turbo, GPT-4)
  - Google Gemini (Gemini 2.5 Flash Preview)
  - DeepSeek (DeepSeek Chat)
- Customizable tone selection
- Easy-to-use Streamlit web interface
- Option to upload or paste job descriptions and personal history
- Download generated cover letters as text files

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/ccomkhj/AI-Cover-Letter-Generator
   cd AI-Cover-Letter-Generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up API keys (optional):
   - Create a `.env` file in the project root directory
   - Add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key
     GOOGLE_API_KEY=your_google_api_key
     DEEPSEEK_API_KEY=your_deepseek_api_key
     ```

## Demo

![Cover Letter Generator Demo](/sample_data/demo.png)

## Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to http://localhost:8501

3. In the web interface:
   - Select your preferred LLM provider and model
   - Enter your API key if not already provided in the `.env` file
   - Choose a tone for your cover letter
   - Upload or paste the job description and your personal history (or leave empty to use sample data)
   - Click "Generate Cover Letter"
   - Download the generated cover letter as a text file

4. Default Data Feature:
   - If you don't provide a job description or personal history, the app will automatically use the sample data
   - A warning message will be displayed indicating that default data is being used
   - This is useful for quickly testing the functionality or seeing how the app works

## Sample Data

The `sample_data` directory contains example files:
- `job_description.txt`: An example job posting for an AI/ML Software Engineer
- `personal_history.txt`: A sample resume and personal history

You can use these files to test the application without creating your own.

## Project Structure

- `app.py`: The main Streamlit web application
- `cover_letter_generator.py`: Core logic for generating cover letters using LangChain
- `requirements.txt`: Python dependencies
- `sample_data/`: Example data files
- `.env`: (Not included) For storing API keys

## Requirements

- Python 3.8+
- Internet connection for accessing LLM APIs
- Valid API keys for the LLM providers you wish to use
