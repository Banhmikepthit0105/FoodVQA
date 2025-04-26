import requests
import pandas as pd
import torch
import os
import csv
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

#pip install -U "huggingface_hub[cli]"
#login with HF token to run: huggingface-cli login

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

def get_predict(question, img_url):

    examples = [
        {"image_path": "Stage 3 model survey/src/fewshot/carbonara.jpeg", "question": "What are the black bits around the carbonara?", "answer": "pepper flakes"},
        {"image_path": "Stage 3 model survey/src/fewshot/curry.jpg", "question": "What color are the fried pork slices?", "answer": "golden-brown"},
        {"image_path": "Stage 3 model survey/src/fewshot/pizza.jpg", "question": "How is the cheese on top of the pizza?", "answer": "melted"},
        {"image_path": "Stage 3 model survey/src/fewshot/rice.jpg", "question": "What is the main protein of the dish?", "answer": "shrimp"},
        {"image_path": "Stage 3 model survey/src/fewshot/sushi.jpg", "question": "Where is the dish?", "answer": "on a plate"}
        # Add more examples here; adjust based on token usage (each image may use ~500 tokens)
    ]

    # Load the images for the examples
    for example in examples:
        example["image"] = Image.open(example["image_path"])
        base_width = 480
        wpercent = (base_width / float(example["image"].size[0]))
        hsize = int((float(example["image"].size[1]) * float(wpercent)))
        example["image"] = example["image"].resize((base_width, hsize), Image.Resampling.LANCZOS)


    image = Image.open(img_url)

    messages = []
    for example in examples:
        messages.append(
            {"role": "user", "content": [{"type": "image", "image": example["image"]}, {"type": "text", "text": example["question"]}]}
        )
        messages.append(
            {"role": "assistant", "content": [{"type": "text", "text": example["answer"]}]}
        )
    messages.append(
        {"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": question}]}
    )
    inputs = processor.apply_chat_template(messages, add_generation_prompt=True)
    

    torch.cuda.empty_cache()
    output = model.generate(**inputs, max_new_tokens=64)
    return processor.decode(output[0])

# File paths
input_csv = 'test_refined.csv'  # Replace with your input CSV path
image_dir = './assets/'         # Directory containing local image files
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
    
    print(image_path)

    base_width = 480
    img = Image.open(image_path)
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img.save('curr.jpg')
    
    # Generate predictions for each question
    question = row["Question"]
    predicted_answer = get_predict( question, 'curr.jpg')
    print(predicted_answer)
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