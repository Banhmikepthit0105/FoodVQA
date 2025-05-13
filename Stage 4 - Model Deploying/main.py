from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from transformers import MllamaForConditionalGeneration, AutoProcessor
from PIL import Image
import torch
import uvicorn
import io

app = FastAPI()

# Load model and processor
model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

def get_prediction(image: Image.Image, question: str) -> str:
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
    ).to(model.device)

    torch.cuda.empty_cache()
    output = model.generate(**inputs, max_new_tokens=64)
    return processor.decode(output[0], skip_special_tokens=True)

@app.post("/predict")
async def predict(question: str = Form(...), file: UploadFile = File(...)):
    try:
        # Load image from uploaded file
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        base_width = 480
        wpercent = (base_width / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)

        # Get prediction
        prediction = get_prediction(image, question)
        return JSONResponse(content={"prediction": prediction})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)