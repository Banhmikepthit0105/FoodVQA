# MODEL TESTING

This folder includes the source code files for running predictions on the test dataset for the following models: Qwen 2.5 VL 7b (zeroshot), MiniCPM-o 2.6 8B (zeroshot), Llama 3.2 11B Vision Instruct (zeroshot and fewshot), Gemini 2.0 flash (zero shot), TF/IDF.

## TESTING A MODEL

For HuggingFace models, they are tested on virtual machine with RTX 3090 24GB graphics card from [thuegpu.vn](https://thuegpu.vn/).

* To run a model, install the necassary packages mentioned on each model card before running the code:
1. (Llama 3.2) [https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct]
2. (MiniCPM) [https://huggingface.co/openbmb/MiniCPM-o-2_6]
3. (Qwen 2.5) [https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct]

* Note that Llama is gated model so you have to request permission to their repository and log into huggingface-cli with a token to be able to run the code.


## POST PROCESSING

After running the test dataset on a HuggingFace model, you should process the predictions to improve the model's evaluation score.

The postprocess uses Gemini's API to extract tokens found in the prediction that are closest in meaning to the ground-truth answer in the test dataset. This reduces the amount of unnecessary tokens in the raw predictions which allow for higher scoring on each evaluation metric.

For more info on the prompting, check out the *postprocess_predictions.py* file.