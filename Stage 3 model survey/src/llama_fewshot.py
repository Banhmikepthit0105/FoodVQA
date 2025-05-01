import requests
import pandas as pd
import torch
import os
import csv
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
from huggingface_hub import login
import re

#pip install -U "huggingface_hub[cli]"
#login with HF token to run: huggingface-cli login

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

def extract_final_answer(decoded_text: str) -> str:
    matches = re.findall(r"assistant\s*\n*(.*?)\s*(?=(user|$))", decoded_text, re.DOTALL)

    if matches:
        final_answer = matches[-1][0].strip()
        return final_answer

    return decoded_text.strip().split("assistant")[-1].strip()

def get_predict(question, img_url):
    examples = [
        {"image_path": "fewshot/carbonara.jpeg", "question": "What are the black bits around the carbonara?", "answer": "pepper flakes"},
        {"image_path": "fewshot/curry.jpg", "question": "What color are the fried pork slices?", "answer": "golden-brown"},
        {"image_path": "fewshot/pizza.jpg", "question": "How is the cheese on top of the pizza?", "answer": "melted"},
        {"image_path": "fewshot/rice.jpg", "question": "What is the main protein of the dish?", "answer": "shrimp"},
        {"image_path": "fewshot/sushi.jpg", "question": "Where is the dish?", "answer": "on a plate"},
        {"image_path": "fewshot/e609b02c4d5e7ea.jpg", "question": "What type of dish is made with shredded cabbage and carrots?", "answer": "coleslaw"},
        {"image_path": "fewshot/b585186ffae6d46.jpg", "question": "What type of containers are used for the mocha coffee?", "answer": "mugs"},
        {"image_path": "fewshot/0646967be05e6a3.jpg", "question": "What color are the brussels sprouts?", "answer": "green"},
        {"image_path": "fewshot/79b48c28aadd2d2.jpg", "question": "Where is the caramel corn located?", "answer": "inside a tin"},
        {"image_path": "fewshot/e9b7023a9f80c83.jpg", "question": "What type of seafood is on the plate?", "answer": "lobster"}
        # Add more examples here; adjust based on token usage (each image may use ~500 tokens)
    ]

    messages = []
    images = []

    for ex in examples:
        img = Image.open(ex["image_path"]).convert("RGB")
        images.append(img)

        qtext = ex["question"].strip()
        qtext += " (Short answer only, max 5 words)"

        messages.append({"role": "user", "content": [{"type": "image"}, {"type": "text", "text": qtext}]})
        messages.append({"role": "assistant", "content": [{"type": "text", "text": ex["answer"]}]})

    img_q = Image.open(img_url).convert("RGB")
    images.append(img_q)
    messages.append({"role": "user", "content": [{"type": "image"}, {"type": "text", "text": question}]})

    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)

    inputs = processor(images=images, text=prompt, return_tensors="pt").to(model.device)

    # Generate
    with torch.no_grad():
        torch.cuda.empty_cache()
        output = model.generate(**inputs, max_new_tokens=64)

    decoded = processor.decode(output[0], skip_special_tokens=True)
    predicted_answer = extract_final_answer(decoded)
    return predicted_answer

# File paths
input_csv = 'test.csv'  # Replace with your input CSV path
image_dir = './test_assets/'         # Directory containing local image files
output_csv = 'llama_fewshot_results.csv'  # Output CSV path

# Read the input CSV into a DataFrame
df = pd.read_csv(input_csv)

# Add columns for predicted answers, initialized as NaN

df['Predicted_Answer'] = pd.NA

# Define output CSV columns
output_columns = [
    'Image', 'Question', 'Answer', 'Predicted_Answer'
]

# Process each row and append to output CSV
if not os.path.isfile(output_csv):
    with open(output_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(output_columns)
df_result = pd.read_csv(output_csv)
processed = []
for index, row in df_result.iterrows():
    processed.append(row['Image'])

for index, row in df.iterrows():
    if index < len(processed):
        continue

    extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

    image_path = None

    for ext in extensions:
        potential_path = os.path.join(image_dir, row['Image'] + ext)
        if os.path.exists(potential_path):
            image_path = potential_path
            break


    if not os.path.isfile(image_path):
        continue
    
    base_width = 480
    img = Image.open(image_path).convert("RGB")
    wpercent = base_width / float(img.size[0])
    hsize = int(float(img.size[1]) * wpercent)
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img.save('curr.jpg')
    
    # Generate predictions for each question
    question = row["Question"]
    predicted_answer = get_predict(question, 'curr.jpg')
    df.at[index, 'Predicted_Answer'] = predicted_answer
    
    # Prepare row data for output
    row_data = [
        row['Image'],
        row['Question'],
        row['Answer'],
        predicted_answer
    ]
        
    with open(output_csv, 'a',) as csvfile:
        writer = csv.writer(csvfile)
        # Write the row to the output CSV
        writer.writerow(row_data)

print(f"Processing complete. Results saved to '{output_csv}'.")