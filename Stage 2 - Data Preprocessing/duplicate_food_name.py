import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm

# Load dataset
df = pd.read_csv('recipes.csv')
food_names = df['Food Name'].dropna().tolist()  # Remove any NaN entries

# Find similar food name pairs
similar_pairs = []
for name in tqdm(food_names, desc="Processing", unit="item"):
    # Exclude the name itself from candidates to prevent self-match
    candidates = [other for other in food_names if other != name]
    
    match = process.extractOne(
        name,
        candidates,
        scorer=fuzz.token_set_ratio,
        score_cutoff=80  # Only consider matches with similarity >= 80
    )
    
    if match:
        matched_name = match[0]
        normalized_score = match[1]  # Score between 0–100
        raw_score = match[2]         # Internal raw similarity score
        similar_pairs.append((name, matched_name, normalized_score, raw_score))

# Create DataFrame from results
matched_df = pd.DataFrame(similar_pairs, columns=['Original', 'Match', 'Normalized_Score', 'Raw_Score'])

# Remove duplicate entries
matched_df = matched_df.drop_duplicates()

# Output results
print("Similar food name pairs (using RapidFuzz):")
print(matched_df.head())

# Save to CSV
matched_df.to_csv('matched_df.csv', index=False)
