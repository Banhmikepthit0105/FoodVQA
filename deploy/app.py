from flask import Flask, render_template, request, jsonify
from models import load_models, generate_chatgpt_answer, generate_gemini_answer
import os
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

@app.route("/load_model", methods=["GET"])
def load_model():
    models = load_models() 
    return jsonify(models)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        question = request.form.get("question")
        selected_model = request.form.get("model")

        if file and question:
            image_data = file.read()
            
            if selected_model == "chatgpt":
                response = generate_chatgpt_answer(question)
            else:
                response = generate_gemini_answer(question, image_data)

            image_base64 = base64.b64encode(image_data).decode("utf-8")
            image_url = f"data:{file.content_type};base64,{image_base64}"

            return jsonify({
                "answer": response,
                "model": selected_model,
                "image_url": image_url
            })
        return jsonify({"error": "Missing image or question"}), 400
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
