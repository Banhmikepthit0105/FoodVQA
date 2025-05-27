## Post-processes model outputs to improve accuracy


import csv
import pandas as pd
import google.generativeai as genai
import os
from time import sleep

key = str(input("Enter your key: ")).strip()
genai.configure(api_key=key)


model = genai.GenerativeModel('models/gemini-2.0-flash-001')
LLM_name = str(input("Enter the model name: ")).strip()

def constraint(question, predict):
    prompt = (
        "You are a helpful VQA assistant.\n"
        "Your task is to extract a single, most relevant answer to the question, based on the given prediction text.\n"
        "The answer must:\n"
        "- Directly address the question's intent\n"
        "- Contain no more than 5 words\n"
        "- Be written entirely in lowercase letters\n"
        "- Not include any commas, lists, or explanations\n"
        "- Be concise and natural, like a typical VQA answer (e.g., 'red shirt', 'top left', 'enchiladas', 'golden-brown', etc.)\n"
        "- If multiple candidates appear in the prediction, select the one most relevant to the question\n"
        "- Respond with only the final answer and nothing else\n\n"
        f"Question: {question}\n"
        f"Predict: {predict}\n"
    )

    response = model.generate_content([prompt])

    return response.text.strip() 


def main():
    input_file = f'{LLM_name}_results.csv'
    output_file = f'{LLM_name}_NEW.csv'

    df = pd.read_csv(input_file)

    headers = ['Image', 'Question', 'Answer', 'Predict']
    dups = []

    if not os.path.isfile(output_file):
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    else:
        existing = pd.read_csv(output_file)
        for _, row in existing.iterrows():
            dups.append(_)
            

    for _,row in df.iterrows():
        
        if _ < len(dups):
            print(f"{row['Image']} {row['Question']}")
            continue

        # output = constraint(row['Answer'], row['Predict'])
        output = constraint(row['Question'], row['Predict'])
        
        print(_, output)

        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    row['Image'],
                    row['Question'],
                    row['Answer'],
                    output,
                ]
            )
        
        sleep(5)


if __name__ == '__main__':
    main()
