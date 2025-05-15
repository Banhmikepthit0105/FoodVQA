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
data_file = './data/cleaned_data_old.csv'
image_folder = 'assets'
output_file = 'img_description_7.csv'



start_row = 3064
end_row = 3580 



start_row_1 = 3581
end_row_1 = 4095



start_row_2 = 4096
end_row_2 = 4611


start_row_3 = 4612
end_row_3 = 5127


start_row_4 = 5128
end_row_4 = 5643

start_row_5 = 5644
end_row_5 = 6128


start_row_6 = 6128
end_row_6 = 6129


#  Missing 380, 4095, 4611, 5127, 5643, 6128 




df = pd.read_csv(data_file)
df = df.iloc[start_row_6:end_row_6]  




extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

genai.configure(api_key='GEMINI_API_KEY')

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('models/gemini-2.0-flash-001')

def create_prompt(food_name='', additional_info=''):
    prompt = (
        f"The following food items are present in this image: {food_name}.\n"
        "Describe the color and relative location of each food item in detail.\n\n"
        # f"Then, look at the summary associate with the image and extract 1 detail (if has) which not exists in the image so that we can use it to make an outside knowledge question:\n{additional_info}"
        # "After all, merge the discription with the info you extract before and summarize all of them with this instruction:"
        "Instruction:\n"
        "- **Only** print the final description, don't print anything else like headers or human-like response!\n"
        "- The summary has maximum 200 words\n"
        "- **Do not** break the line!\n"
    )
    
    return prompt

file_exists = os.path.exists(output_file)

if not file_exists:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image', 'Image description'])

print('Generate...')

for i in range(200, 1532):
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

print("Processing completed!")