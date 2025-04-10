from openai import OpenAI
import os
import csv
import time
import pandas as pd
DEEPSEEK_API_KEY = ""
data_file = 'sample_output.csv'
output_file = "output_QApairs_nghia.csv"
df = pd.read_csv(data_file)
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
def create_prompt(summary, keywords):
    prompt = (
        f"Based on these following key words:\n"
        f"{keywords}\n"
        f"And the food image description: {summary}\n"
        "Please generate **one simple question per keyword** where:\n"
        "1.Each question is based on the food image description.\n"
        "2.The answer to each question must **exactly match its corresponding keyword**\n"
        "3.The number of questions must be equal to the number of keywords\n"
        "4.For keywords that are prepositions (e.g., on the table), ask a **Where** question.\n"
        "5.**The order of the questions must match the order of the keywords**.\n"
        "Instruction:\n"
        "- Generate **only** the questions as a comma-separated list.\n"
        "- Do not include headers, explanations, or human-like responses.\n"
    )
    return prompt
file_exists = os.path.exists(output_file)
if not file_exists:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image', 'Image description', 'Keywords', 'Questions'])
print('Generating keywords...')
for index in range(3049, len(df)):
    row = df.iloc[index]
    image_id = str(row['Image']).strip()
    description = row.get('Image description', '')
    _keywords = row.get('Keywords', '')
    prompt = create_prompt(summary=description, keywords=_keywords)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an AI that generates questions about food images for VQA tasks"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    
    questions = response.choices[0].message.content.strip() if response.choices and response.choices[0].message.content else "NaN"
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([image_id, description, _keywords, questions])  
    print(f"Processed: {image_id}")
    time.sleep(2)  

print("Processing completed!")

