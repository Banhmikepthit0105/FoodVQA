# METRICS AND PREDICTIONS
These folder include the predictions results of explored models and evaluation results of metrics such as: BLEU, ROUGE-1, ROUGE-2, ROUGH-L and GPTScore.

## METRICS

This folder includes:
1. Two jupyter notebooks used for running the evaluation metrics. The two version differ in how GPTScore is prompted, the other metrics remain unchanged.
2. Two result folder containing .csv files that are results of evaluation. Each file contains scores of a metric for a model's predictions

To run the evaluation notebooks, simply change the filepaths, filenames and run each code block in order.
For GPTScore, make sure to add your own API key.

For information on how each metric works, the notebooks contain explanations for each metric.

## PREDICTIONS

This folder includes:
1. *model_outputs* which contains raw prediction results from each model on the test dataset.
2. *processed_outputs* which contains processed prediction results from *model_output*.

Tested models: Qwen 2.5 VL 7b (zeroshot), MiniCPM-o 2.6 8B (zeroshot), Llama 3.2 11B Vision Instruct (zeroshot and fewshot), Gemini 2.0 flash (zero shot), TF/IDF, BEiT-3 (finetuned), LXMERT

You can find more information on the source code for each model and output postprocess in the *src* folder.