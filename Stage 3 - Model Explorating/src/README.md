# MODEL TESTING

This folder includes the source code files for running predictions on the test dataset for the following models: Qwen 2.5 VL 7b (zeroshot), MiniCPM-o 2.6 8B (zeroshot), Llama 3.2 11B Vision Instruct (zeroshot and fewshot), Gemini 2.0 flash (zero shot), TF/IDF, BEiT-3, and LXMERT.

## TESTING A MODEL

For HuggingFace models, they are tested on virtual machine with RTX 3090 24GB graphics card from [thuegpu.vn](https://thuegpu.vn/).

* To run a model, install the necassary packages mentioned on each model card before running the code:
1. (Llama 3.2) [https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct]
2. (MiniCPM) [https://huggingface.co/openbmb/MiniCPM-o-2_6]
3. (Qwen 2.5) [https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct]

* The output of each code is a csv with coloumns of: Image, Question, Answer, Predicted_Answer.

* Note that Llama is gated model so you have to request permission to their repository and log into huggingface-cli with a token to be able to run the code.


### RUNNING LLAMA ZEROSHOT AND FEWSHOT

After obtaining permission, install the following dependencies:

```bash
pip install pandas torch torchvision transformers accelerate Pillow huggingface_hub[cli]
```

Then login into huggingface-cli with your token by running:
```bash
huggingface-cli login
```

Replace the folder path to the test dataset and image folder to run the file:
```bash
python evaluate_llama_zeroshot.py
```
or
```bash
python evaluate_llama_fewshot.py
```

### RUNNING QWEN

Install the following dependencies:

```bash
pip install pandas torch torchvision transformers accelerate Pillow qwen-vl-utils[decord]==0.0.8
```

Replace the folder path to the test dataset and image folder to run the file:
```bash
python evaluate_qwen.py
```

### RUNNING MINICPM

Install the following dependencies:

```bash
pip install pandas torch torchaudio torchvision transformers==4.44.2 accelerate Pillow librosa soundfile vocos decord moviepy vector-quantize-pytorch
```

Replace the folder path to the test dataset and image folder to run the file:
```bash
python eval_MiniCPM.py
```

### RUNNING GEMINI

Install the following dependencies:

```bash
pip install google-genai Pillow pandas
```
Replace the folder path to the test dataset and image folder, add a Gemini API key to run the file:
```bash
python evaluate_gemini_zeroshot.py
```

### RUNNING BEIT-3

Install BEiT-3 checkpoint from this [link](https://github.com/microsoft/unilm/blob/master/beit3/README.md).
* We recommend using the `beit3_base_indomain_patch16_224` pre-trained model, which has been tested on the VQAv2 dataset.

Once the model is downloaded, simply run the provided notebook to fine-tune and evaluate it on your task.

### RUNNING LXMERT

1. **Visual Feature Extraction:**
   Begin by running the Faster R-CNN model to extract region-based visual features from all images in the training set. These features will be serialized and stored as `.pkl` files for efficient loading during training.

2. **Model Fine-Tuning and Evaluation:**
   After feature extraction, proceed to run the fine-tuning pipeline. This step will adapt the model to your specific task and dataset, followed by evaluation to measure its performance.


## POST PROCESSING

After running the test dataset on a HuggingFace model, you should process the predictions to improve the model's evaluation score.

The postprocess uses Gemini's API to extract tokens found in the prediction that are closest in meaning to the ground-truth answer in the test dataset. This reduces the amount of unnecessary tokens in the raw predictions which allow for higher scoring on each evaluation metric.

For more info on the prompting, check out the *postprocess_predictions.py* file.
