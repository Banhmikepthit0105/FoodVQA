# Food-VQA: Data Preprocessing Stage

## Setup for Data Preprocessing

```bash
git clone https://github.com/Banhmikepthit0105/FoodVQA.git
cd FoodVQA

pip install -r requirements.txt
```
### 1. Initial Data Cleaning

First, clean the raw recipe data:

```bash
python clean_recipe_data.py
```

This script:
- Processes the raw data from `Stage 1 - Data Collecting/output_sitemap/recipes.csv`
- Cleans text fields
- Removes duplicate entries
- Saves the cleaned data to a file `./data/raw/foodvqa_before_img_quality.csv`

### 2. Filtering samples by quality

Run the Jupyter notebook for exploratory data analysis and quality filtering:


This notebook will processes the raw data from `./data/raw/foodvqa_1before_img_qualityFilter.csv`


```bash
jupyter notebook datapreprocessing.ipynb
```

This notebook will:
- Select high-quality samples based on:
  - Number of distinct samples
  - Calories
  - Image quality (pixel dimensions, clarity)
  - Dish popularity

After preprocessing, you should have:
- `data/raw/foodvqa_2after_img_qualityFilter.csv` 

### 3. Generate Image Descriptions

Generate detailed descriptions for each food image using Google's Gemini API:

```bash
python gemini_img_captioning.py
```

Before running:
1. Set up your Gemini API key in the script
2. Ensure your images are in the 'assets' folder (or modify the path in the script)
3. Prepare the input CSV file ('cleaned_data_old.csv' by default)

This script:
- Processes each image using Gemini API
- Generates concise descriptions (max 5 words)
- Saves image IDs and descriptions to 'img_description.csv'
- Includes a delay between API calls to respect rate limits

After image captioning, you should have:
- `data/raw/foodvqa_img_description.csv` containing description for the image data.

### 4. Extract Keywords from Image Descriptions

Extract important keywords from the image descriptions using Google's Gemini API:

```bash
python gemini_extract_keywords.py
```

Before running:
1. Set up your Gemini API key in the script
2. Ensure the image descriptions CSV is available ('Thai_img_description.csv' by default, but you should modify this to use `data/raw/foodvqa_img_description.csv`)

This script:
- Processes each image description using Gemini API
- Extracts 6 diverse keywords including verbs, adjectives, nouns, colors, and prepositions
- Saves image IDs, descriptions, and keywords to a CSV file
- Includes a delay between API calls to respect rate limits

After keyword extraction, you should have:
- `data/raw/foodvqa_keywords.csv` containing image IDs, descriptions, and extracted keywords

### 5. Generate QA Pairs 

Generate question-answer pairs from the image descriptions and keywords:

```bash
python gemini_generate_qa_pairs.py
```

Before running:
1. Set up your Gemini API key in the script
2. Ensure the image descriptions and keywords CSVs are available

This script:
- Uses descriptions and keywords as context for Question generation
- Uses the keywords as the Answer of that Question
- Then, it creates diverse 5 Question-Answer pairs using the Gemini API
- Generates multiple question types and appropriate answers
- Outputs to CSV format for model training

After QA pair generation, you should have:
- `data/raw/foodvqa_QApairs.csv` containing question-answer pairs for each image

### 6. Create Final Dataset and Train/Val/Test Splits

After generating all the QA pairs, you need to create the final dataset and split it for training:

```bash
python create_final_dataset.py
```

This script:
1. Combines image information with QA pairs
2. Performs any necessary cleaning and formatting
3. Creates the final `foodvqa.csv` with all required fields:
   - Image ID/path
   - Image description
   - Keywords
   - Question
   - Answer
   - Additional metadata

After creating the final dataset, split it into train/validation/test sets:

```bash
python split_dataset.py
```

This script:
- Splits the data with a 70/15/15 ratio by number of images (not QA pairs)
- Ensures no image overlap between splits (all QA pairs for the same image go into the same split)
- Saves three separate CSV files:
  - `data/processed/train.csv` (70% of images)
  - `data/processed/validation.csv` (15% of images)
  - `data/processed/test.csv` (15% of images)

### 7. Dataset Analysis

Analyze the dataset to understand its characteristics:

```bash
jupyter notebook dataset_analysis.ipynb
```

This notebook creates:
- Bar charts of word count distributions
- Word clouds showing frequent terms in questions and answers
- Pie charts of question types (What, How, Is, etc.)

All visualizations are saved to:
- `data-overview-analysis/new/bar_chart_distribution/`
- `data-overview-analysis/new/world_cloud/`
- `data-overview-analysis/new/pie_chart/`

### 8. Filtering Answers by Length

Filter answers to limit their length (important for model training):

```bash
python filter_answers_by_length.py
```

This script:
- Reads the dataset from `./data/raw/train.csv`
- Keeps only QA pairs where answers are 5 words or less
- Saves the filtered data back to `./data/raw/train.csv`
- Apply the process to validation.csv and test.csv