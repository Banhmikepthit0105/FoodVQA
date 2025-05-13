from flask import Flask, request, render_template, jsonify
import os
from io import BytesIO
from PIL import Image
import base64
import requests
import re

# Import existing models
from models import load_models, generate_chatgpt_answer, generate_gemini_answer

app = Flask(__name__, 
            static_folder="static", 
            template_folder="templates")

# Replace with your ngrok URL (no trailing slash)
ngrok_url = "https://c2b6-103-78-3-96.ngrok-free.app/"

# Set Llama availability
llama_available = True  # Since we're using external API

def get_llama_prediction(image: Image.Image, question: str) -> str:
    try:
        # Convert PIL image to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format=image.format or 'JPEG')
        img_byte_arr.seek(0)
        
        # Prepare data for ngrok request
        files = {
            "file": ("image.jpg", img_byte_arr, "image/jpeg")
        }
        data = {
            "question": question
        }
        
        # Make request to ngrok server
        response = requests.post(f"{ngrok_url}/predict", data=data, files=files)
        response.raise_for_status()
        prediction = response.json().get("prediction", "No prediction received")
        parts = re.split(r'assistant', prediction, flags=re.IGNORECASE)
        prediction = parts[1][2:]
        print("Prediction: ", prediction)
        return prediction
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Llama API: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/load_model")
def load_model():
    models = load_models()
    if llama_available:
        models["Llama 3.2"] = "llama-3.2"
    return jsonify(models)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def process_question():
    try:
        question = request.form.get("question")
        model = request.form.get("model")
        image_file = request.files.get("image")
        
        if not image_file or not question or not model:
            return jsonify({"error": "Missing required fields"}), 400
        
        image_data = image_file.read()
        
        if model == "chatgpt":
            response = generate_chatgpt_answer(question)
        elif model == "llama-3.2" and llama_available:
            pil_image = Image.open(BytesIO(image_data))
            response = get_llama_prediction(pil_image, question)
            print(response)
        else:
            # Default to gemini
            response = generate_gemini_answer(question, image_data)

        image_base64 = base64.b64encode(image_data).decode("utf-8")
        image_url = f"data:{image_file.content_type};base64,{image_base64}"

        return jsonify({
            "answer": response,
            "model": model,
            "image_url": image_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# For direct execution
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
