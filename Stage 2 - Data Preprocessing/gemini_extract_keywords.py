import os
import pandas as pd
import csv
import time
import pathlib
import textwrap
import google.generativeai as genai
import re
from PIL import Image

# Define file paths
data_file = 'Thai_img_description.csv'
output_file = 'output_keywords_6.csv'

# Load dataset




start_row = 90
end_row = 511



start_row_1 = 558
end_row_1 = 1022



start_row_2 = 1060
end_row_2 = 1533


start_row_3 = 1676
end_row_3 = 2044


start_row_4 = 2086
end_row_4 = 2555

start_row_5 = 3064
end_row_5 = 3065


# start_row_6 = 6128
# end_row_6 = 6129



df = pd.read_csv(data_file)
df = df.iloc[start_row_5:end_row_5]  




genai.configure(api_key='AIzaSyCVnxj23aT141yrEjMPt-uyW-v0AvBwc1E')



# Initialize Gemini model
model = genai.GenerativeModel('models/gemini-2.0-flash-001')

def create_prompt(summary=''):
    prompt = (
        f"Given a summary of an image for the VQA task, extract the top 6 important keywords, ensuring diversity in word types, "
        f"including at least one verb, one adjective, one noun, one color, and one preposition (if present).\n\n"
        f"Summary: {summary}\n\n"
        "Instruction:\n"
        "- **Only** print the extracted keywords as a comma-separated list.\n"
        "- If there is a preposition, include the full phrase containing it (e.g., 'on the table' instead of just 'on').\n"
        "- Do not print anything else like headers or human-like responses!\n"
    )
    return prompt


file_exists = os.path.exists(output_file)
if not file_exists:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image', 'Image description', 'Keywords'])

print('Generating keywords...')

for index, row in df.iterrows():
    image_id = str(row['Image']).strip()
    description = row.get('Image description', '')
    
    prompt = create_prompt(summary=description)
    
    response = model.generate_content(prompt)
    
    keywords = response.text.strip() if response and response.text else "NaN"
    
    # Write to output file
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([image_id, description, keywords])
    
    print(f"Processed: {image_id}")
    
    time.sleep(5)


print("Processing completed!")