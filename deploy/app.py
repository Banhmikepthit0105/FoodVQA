from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from io import BytesIO
from PIL import Image
import base64

# Import existing models
from models import load_models, generate_chatgpt_answer, generate_gemini_answer

# Import Llama model from main.py
from transformers import MllamaForConditionalGeneration, AutoProcessor
import torch

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load Llama model
model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
try:
    llama_model = MllamaForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(model_id)
    llama_available = True
except Exception as e:
    print(f"Could not load Llama model: {e}")
    llama_available = False

def get_llama_prediction(image: Image.Image, question: str) -> str:
    if not llama_available:
        return "Llama model not available"
    
    messages = [
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": question}
        ]}
    ]
    input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(
        image,
        input_text,
        add_special_tokens=False,
        return_tensors="pt"
    ).to(llama_model.device)

    torch.cuda.empty_cache()
    output = llama_model.generate(**inputs, max_new_tokens=64)
    return processor.decode(output[0], skip_special_tokens=True)

@app.get("/load_model")
async def load_model():
    models = load_models()
    if llama_available:
        models["Llama 3.2"] = "llama-3.2"
    return models

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def process_question(
    question: str = Form(...),
    image: UploadFile = File(...),
    model: str = Form(...)
):
    try:
        image_data = await image.read()
        
        if model == "chatgpt":
            response = generate_chatgpt_answer(question)
        elif model == "llama-3.2" and llama_available:
            pil_image = Image.open(BytesIO(image_data))
            response = get_llama_prediction(pil_image, question)
        else:
            # Default to gemini
            response = generate_gemini_answer(question, image_data)

        image_base64 = base64.b64encode(image_data).decode("utf-8")
        image_url = f"data:{image.content_type};base64,{image_base64}"

        return {
            "answer": response,
            "model": model,
            "image_url": image_url
        }
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

# For direct execution
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
