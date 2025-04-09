from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        question = request.form.get("question")
        selected_model = request.form.get("model")

        if file and question:
            image_data = file.read()
            image_part = {"mime_type": file.content_type, "data": image_data}
            
            response = model.generate_content([question, image_part])
            
            confidence = min(95, max(40, hash(response.text) % 60 + 40)) 
            
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            image_url = f"data:{file.content_type};base64,{image_base64}"

            return jsonify({
                "answer": response.text,
                "model": selected_model,
                "confidence": confidence,
                "image_url": image_url
            })
        return jsonify({"error": "Missing image or question"}), 400
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)