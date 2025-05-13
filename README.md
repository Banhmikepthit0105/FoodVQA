# FoodieVQA

An end-to-end automated pipeline for constructing and evaluating food-specific Visual Question Answering datasets.

## Overview

FoodieAutoGe-VQA is a framework that:
1. Collects food images and descriptions
2. Generates QA pairs using LLMs
3. Evaluates multiple VQA approaches on food domain data

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

### API Keys
The following API keys need to be set up:
- DeepSeek API (for QA generation)
- OpenAI API (for GPTScore evaluation)
- Gemini API (for zero-shot evaluation)
- Hugging Face token (for accessing models)

## Usage

### Stage 1: Data Collection
```bash
# Crawl food images and descriptions
python food_image_crawler.py

# Filter answers by length
python filter_answers_by_length.py
```

### Stage 2: Data Preprocessing
```bash
# Clean recipe data
python clean_recipe_data.py

# Generate QA pairs from descriptions
python generate_qa_pairs.py

# Analyze dataset statistics
python dataset_analysis.py
```

### Stage 3: Model Evaluation
```bash
# Run baseline TF-IDF model
python baseline_tfidf.py

# Run zero-shot models
python evaluate_gemini_zeroshot.py
python evaluate_llama_zeroshot.py
python evaluate_qwen.py

# Run fine-tuned models
python evaluate_beit3.py

# Calculate evaluation metrics
python evaluate_metrics.py --input results/predictions/raw/model_predictions.csv --output results/metrics/

# Post-process model outputs
python postprocess_predictions.py
```

## Evaluation Metrics

This project uses multiple evaluation metrics:

### BLEU Score
- Measures n-gram precision between predicted and reference answers
- Command: `python evaluate_metrics.py --metric bleu`

### ROUGE Score
- Measures recall-oriented n-gram overlap
- Command: `python evaluate_metrics.py --metric rouge`

### GPTScore
- Uses GPT to evaluate semantic similarity between answers
- Command: `python evaluate_metrics.py --metric gptscore`

### Exact Match, Precision, Recall, F1
- Exact Match: 1 if prediction exactly matches reference, 0 otherwise
- Precision: Fraction of predicted tokens that appear in reference
- Recall: Fraction of reference tokens captured in prediction
- F1: Harmonic mean of precision and recall
- Command: `python evaluate_metrics.py --metric em_prf1`

## Dataset Structure

The dataset consists of:
- Food images in JPG format
- CSV files with image IDs, questions, and answers
- Train/test splits organized by image ID
