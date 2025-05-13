import ast
import pandas as pd

def parse_line(line):
    """
    Parse a line of the CSV and return a tuple:
      (image, food_name, summary, ingredients, calories)
    or return None if any part is missing or the ingredient list is malformed.
    """
    line = line.strip()
    
    # 1. Image: from start to the first comma.
    image_end = line.find(',')
    if image_end == -1:
        return None
    image = line[:image_end].strip()
    remaining = line[image_end+1:]
    
    # 2. Food Name: from the first comma to the second comma.
    food_end = remaining.find(',"')
    if food_end == -1:
        return None
    food_name = remaining[:food_end].strip()
    remaining = remaining[food_end+1:]
    
    # 3. Summary: from the beginning of the summary (should start with a double quote)
    #    to the sequence '",' which marks the end of the summary.
    if not remaining.startswith('"'):
        return None
    summary_end = remaining.find('",[')
    if summary_end == -1:
        return None
    # Remove the surrounding double quotes.
    summary = remaining[1:summary_end].strip()
    remaining = remaining[summary_end+2:]  # Skip over the closing quote and comma.
    
    # 4. Ingredient list: should start with a '['.
    ing_start = remaining.find('[')
    if ing_start == -1:
        return None
    
    # Use a counter to find the matching closing bracket.
    counter = 0
    ing_end = None
    for i, ch in enumerate(remaining[ing_start:]):
        if ch == '[':
            counter += 1
        elif ch == ']':
            counter -= 1
            if counter == 0:
                ing_end = ing_start + i
                break
    if ing_end is None:
        return None
    ing_str = remaining[ing_start:ing_end+1].strip()
    
    # 5. Calories: from the last comma in the remaining text to the end.
    remaining_after_ing = remaining[ing_end+1:]
    last_comma = remaining_after_ing.rfind(',')
    if last_comma == -1:
        return None
    calories_str = remaining_after_ing[last_comma+1:].strip()
    try:
        calories = int(calories_str)
    except ValueError:
        calories = None

    # Validate the ingredient list by trying to parse it.
    try:
        ingredients = ast.literal_eval(ing_str)
        if not isinstance(ingredients, list):
            return None
    except Exception:
        return None
    
    return image, food_name, summary, ingredients, calories

# Process the file line by line and accumulate valid rows.
data = []
input_file = "output.csv"  # Change to your filename
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        parsed = parse_line(line)
        if parsed is not None:
            data.append(parsed)
        # If parsed is None, the line is skipped (invalid ingredient format, etc.)

df = pd.DataFrame(data, columns=["Image", "Food Name", "Summary", "Ingredients", "Calories"])
df.to_csv("recipes.csv", index=False)


print(df)
