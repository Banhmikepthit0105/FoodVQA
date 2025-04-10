import os
import pandas as pd
import csv
import time
import pathlib
import textwrap
import google.generativeai as genai
import re
import PIL.Image

# parent folder of the csv files
data_file = 'cleaned_data_old.csv'
image_folder = 'assets'
output_file = 'img_description.csv'

df = pd.read_csv(data_file, delimiter=" ")
# df = df.dropna(subset=['Food Name'])

extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

genai.configure(api_key='')

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('models/gemini-2.0-flash-001')

def create_prompt(food_question='', additional_info=''):
    prompt = (
        f"In the image,{food_question}.\n"
        "Instruction:\n"
        "- **Only** print the final description, don't print anything else like headers or human-like response!\n"
        "- The answer has maximum 5 words\n"
    )
    
    return prompt

file_exists = os.path.exists(output_file)

if not file_exists:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image', 'Image description'])

print('Generate...')

for i in range(len(df)):
    row = df.iloc[i]
    image_id = str(row['Image']).strip()
    image_path = None
    for ext in extensions:
        potential_path = os.path.join(image_folder, image_id + ext)
        if os.path.exists(potential_path):
            image_path = potential_path
            continue

    if not image_path:
        print(f"Cannot find image with ID: {image_id}")
        continue

    image = PIL.Image.open(image_path)
    prompt = create_prompt(
        food_name = row['Food Name'],
        additional_info = row['Summary']
    )

    response = model.generate_content([prompt, image])

    if response and response.text:
        summary = response.text.strip()
    else:
        summary = "NaN"

    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([image_id, summary])

    print(f"Processed: {image_path}")

    time.sleep(5)
    # if index == 10:
    #     break

print("Processing completed!")