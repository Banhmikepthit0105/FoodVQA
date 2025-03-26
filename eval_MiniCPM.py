import pandas as pd
from PIL import Image
import os
import torch
from transformers import AutoModel, AutoTokenizer

## REQUIREMENT: pip install vector_quantize_pytorch vocos

def main():
    error_counter = 0
    image_dir = '/root/Users/Vuong/Downloads/archive/assets/assets'
    test_path = '/root/test_refined.csv'

    test_df = pd.read_csv(test_path, header=0)
    result_df = pd.DataFrame(columns=['Image', 'Question', 'Answer', 'Predict'])
    image_extensions = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = AutoModel.from_pretrained(
        'openbmb/MiniCPM-o-2_6',
        trust_remote_code=True,
        attn_implementation='sdpa',
        torch_dtype=torch.bfloat16,
        init_vision=True,
        init_audio=True,
        init_tts=True
    ).to(device).eval()

    tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-o-2_6', trust_remote_code=True)

    # Loop each row
    for idx, row in test_df.iterrows():
        img_name = row['Image']
        image_path = None
        
        for ext in image_extensions:
            temp_path = os.path.join(image_dir, f"{img_name}{ext}")
            if os.path.exists(temp_path):
                image_path = temp_path
                break
        
        if image_path is None:
            error_counter += 1
        
        img = Image.open(image_path).convert('RGB')
        base_width = 480
        wpercent = (base_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
        img.save('curr.jpg')
        image = Image.open('curr.jpg').convert('RGB')

        question = row['Question']
        true_answer = row['Answer']
        
        msgs = [{'role': 'user', 'content': [image, question]}]
        predict = model.chat(msgs=msgs, tokenizer=tokenizer)
        
        result_df.loc[idx] = [img_name, question, true_answer, predict]
        
    result_df.to_csv('answer_MiniCPM.csv', index=False)
    print(error_counter)
    print(result_df)

if __name__ == "__main__":
    main()