# FoodVQA - Food Visual Question Answering

A visual question answering system specialized for food images that allows users to upload food photos and ask questions about them. The system can use multiple AI models to generate answers.

## Features

- Upload food images and ask questions about them
- Choose between multiple AI models:
  - ChatGPT (OpenAI)
  - Gemini 2.0 (Google)
  - Llama 3.2 (Meta)
- Modern user interface with real-time preview

## Setup

1. Clone the repository

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# For Windows
set OPENAI_API_KEY=your_openai_api_key
set GEMINI_API_KEY=your_gemini_api_key

# For Linux/Mac
export OPENAI_API_KEY=your_openai_api_key
export GEMINI_API_KEY=your_gemini_api_key
```

## Running the Application

Run the application using:
```bash
python app.py
```

The application will be available at http://localhost:8000

## Project Structure

- `app.py`: Main FastAPI application
- `models.py`: Model integration for ChatGPT and Gemini
- `templates/`: HTML templates for the frontend
- `static/`: Static files (CSS, JavaScript, images)

## API Endpoints

- `GET /`: Main page with the UI
- `GET /load_model`: Get available models
- `POST /`: Process an image and question using the selected model

## Requirements

- Python 3.8+
- FastAPI
- Jinja2
- Uvicorn
- OpenAI API key (for ChatGPT)
- Google Gemini API key (for Gemini)
- Transformers library (for Llama model) 