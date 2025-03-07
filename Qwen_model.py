import pandas as pd
import os
import csv
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
#pip install git+https://github.com/huggingface/transformers accelerate
#pip install qwen_vl_utils

# if jinja2 error
# pip install jinja2 --upgrade

# Load the model and processor
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct", torch_dtype="auto", device_map="auto"
)
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")


def get_qwen_vl_prediction(image_path, question):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {"type": "text", "text": question},
            ],
        }
    ]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    return output_text[0]

# File paths
input_csv = 'test.csv'  # Replace with your input CSV path
image_dir = 'assets'         # Directory containing local image files
output_csv = 'output_results.csv'  # Output CSV path

# Read the input CSV into a DataFrame
df = pd.read_csv(input_csv, sep=' ')

# Add columns for predicted answers, initialized as NaN

df['Predicted_Answer'] = pd.NA

# Define output CSV columns
output_columns = [
    'Image', 'Question', 'Answer', 'Predicted_Answer'
]

# Write header to output CSV
with open(output_csv, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(output_columns)

# Process each row and append to output CSV
with open(output_csv, 'a',) as csvfile:
    writer = csv.writer(csvfile)
    for index, row in df.iterrows():
        image_filename = row['Image'] + ".jpg"

    
        image_path = os.path.join(image_dir, image_filename)
        print(image_path)

        if not os.path.isfile(image_path):
            continue
        
        # Generate predictions for each question
        question = "Answer the following question in the shortest amount of words possible. " + row["Question"]
        predicted_answer = get_qwen_vl_prediction(image_path, question)
        print(predicted_answer)
        df.at[index, 'Predicted_Answer'] = predicted_answer
        
        # Prepare row data for output
        row_data = [
            row['Image'],
            row['Question'],
            row['Answer'],
            row['Predicted_Answer']
        ]
        
        # Write the row to the output CSV
        writer.writerow(row_data)

print(f"Processing complete. Results saved to '{output_csv}'.")