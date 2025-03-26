import requests
import pandas as pd
import torch
import os
import csv
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

def get_predict(question, img_url):

    image = Image.open(img_url)

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
    return processor.decode(output[0])

# File paths
input_csv = '/root/test_refined.csv'  # Replace with your input CSV path
image_dir = '/root/Users/Vuong/Downloads/archive/assets/assets'         # Directory containing local image files
output_csv = 'llama_results.csv'  # Output CSV path

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
    if row['Image'] in processed:
        continue

    image_filename = row['Image'] + ".jpg"


    image_path = os.path.join(image_dir, image_filename)
    print(image_path)

    if not os.path.isfile(image_path):
        continue
    
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