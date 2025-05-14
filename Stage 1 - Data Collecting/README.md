# Food-VQA: Data Collection Stage

This README covers the data collection stage of the Food-VQA project. It provides instructions on how to crawl recipe links and download food images from those links.

## Setup for Data Collection

### Environment Requirements
```bash
# Clone the repository
git clone https://github.com/Banhmikepthit0105/FoodVQA.git
cd FoodVQA

# Install required packages
pip install -r requirements.txt
```
## Data Collection Process

### 1. Crawling Recipe Links

First, you need to collect recipe URLs from sitemaps:

```bash
python food_image_crawler.py --mode sitemap
```

This will collect URLs from recipe websites and save them to a file. Sample sitemap links are provided in `links/urlsRecipe_sitemap1.txt` for demonstration purposes.

### 2. Crawling Food Images from Recipe Links

Once you have collected recipe links, you can crawl images from these URLs:

```bash
python food_image_crawler.py --mode crawl
```

This will:
- Read the recipe URLs from the file
- Visit each recipe page
- Extract food images
- Save them to the `crawled_images` directory
- Each image is named using a unique ID generated from the dish name


### 3. Merging files

Once the outputs for sitemap are crawled, then a python code will be created to merge them. The entire dataset will be stored at `./State 2 - Data Preprocessing/raw/recipes.txt`


## Notes

- The crawler is configured for specific recipe websites. You might need to adjust the CSS selectors in the code if you're crawling from different sites.

- If you encounter connection issues or timeouts, try adding delays between requests or using a proxy.

- Some sample links are provided in `links/urlsRecipe_sitemap1.txt` for demonstration purposes. For a full dataset, you will need to access the entire folder `links`.