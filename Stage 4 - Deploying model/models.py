# models.py
import openai
import google.generativeai as genai
import os
from PIL import Image
import io

openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_models():
    available_models = {
        "ChatGPT": "chatgpt",
        "Gemini 2.0": "gemini-2.0-flash-001"
    }
    return available_models

def generate_chatgpt_answer(question):
    response = openai.Completion.create(
        model="gpt-4",  

        
        prompt=question,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def generate_gemini_answer(question, image_data):
    image = Image.open(io.BytesIO(image_data))
    prompt = (
        f"In the image,{question}.\n"
        "Instruction:\n"
        "- **Only** print the final answer, don't print anything else like headers or human-like response!\n"
        "- The answer has maximum 5 words\n"
    )
    response = genai.GenerativeModel("gemini-2.0-flash-001").generate_content([prompt, image])
    return response.text.strip() if response and response.text else "No response from Gemini model"
