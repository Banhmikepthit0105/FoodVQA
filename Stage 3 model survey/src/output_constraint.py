import csv
import pandas as pd
import google.generativeai as genai
import os
from time import sleep


genai.configure(api_key='')


model = genai.GenerativeModel('models/gemini-2.0-flash-001')

def constraint(answer, predict):
    prompt = (
        'You are a helpful assistant.\n'

        'Your task is to extract the words from the generated text of "Predict" that is as close as possible in meaning to the ground truth text of "Answer".\n'

        'If there are words in "Predict" that is an exact match with "Answer", return those words as extracted words.\n'

        'The length of the extracted words must only 5 words or less.\n'

        'In case you can not find words that are remotely close in meaning, the extracted words should at least match the ground truth words in type. For example, if the ground truth are adjectives then the extracted words must also be adjectives.\n'

        'Respond with only the extracted words and nothing else.\n'

        f'Predict: {predict}\n'

        f'Answer: {answer}'
    )
    
    response = model.generate_content([prompt])

    return response.text.strip() 


def main():
    input_file = 'llama_results.csv'
    output_file = 'llama_NEW.csv'

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

        output = constraint(row['Answer'], row['Predict'])
        
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
        
        sleep(1)


if __name__ == '__main__':
    main()