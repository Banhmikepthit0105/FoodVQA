import pandas as pd

file_path = r"./data/clean data/validation.csv"
output_path = r"./data/trimmed/clean data/trimmed_validation.csv"

df = pd.read_csv(file_path)
ans_col = ['Answer']

# Function to count words in a string
def count_words(s):
    if pd.isna(s):
        return 0
    return len(s.split())

# Filtering rows with answers longer than 5 words
filtered_df = df[df[ans_col].applymap(count_words).max(axis=1) <= 5]
filtered_df.to_csv(output_path, index=False)

# Check the max number of words in the answer column(s) in the original and filtered data
print("Original data (max word count per column):")
print(df[ans_col].apply(lambda x: x.apply(count_words)).max())

print("\nFiltered data (max word count per column):")
print(filtered_df[ans_col].apply(lambda x: x.apply(count_words)).max())