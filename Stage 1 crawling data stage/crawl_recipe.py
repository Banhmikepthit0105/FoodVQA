import hashlib



import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



def generate_image_id(dish_name):
    hash_object = hashlib.sha256(dish_name.encode())
    image_id = hash_object.hexdigest()[:15]  
    return image_id

def remove_spaces(text):
    return text.replace(" ", "")

def convert_dishname_to_id(dish_name):
    remove_spaces(dish_name)
    _id = generate_image_id(dish_name)
    return _id


def get_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def crawl_recipe(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Referer': 'https://www.allrecipes.com/', 
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        with open("crawled_urls.txt", "a", encoding="utf-8") as file:
            file.write(f"{url}\n")


    # if url:
    #     driver = get_selenium_driver()

    #     driver.get(url) 

    #     time.sleep(1)  
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')


#===========================================================================================================
        _title = ""
        if soup.find('h1', class_='article-heading text-headline-400'):
          _title = soup.find('h1', class_='article-heading text-headline-400').get_text(strip=True)
        print(f"Title: {_title}")


#===========================================================================================================
        _subheading = soup.find('p', class_='article-subheading text-body-100')
        if _subheading:
            _subheading = _subheading.get_text(strip=True)
            print(f"Summary: {_subheading}")
        else:
            print("Không có tóm tắt, bỏ qua trang này.")
            print("================================================================")
            time.sleep(1)
            return None

#===========================================================================================================

        list_ingredients = []
        ingredients = soup.find_all('li', class_='mm-recipes-structured-ingredients__list-item')
        for ingredient in ingredients:
            name = ingredient.find('span', {'data-ingredient-name': 'true'}).get_text(strip=True) if ingredient.find('span', {'data-ingredient-name': 'true'}) else ""
            list_ingredients.append(name)
        print(f"Ingredients: {list_ingredients}")


#===========================================================================================================

        _calories = soup.find('tr', class_='mm-recipes-nutrition-facts-summary__table-row')
        if _calories:
            _calories = _calories.find_all('td')[0].get_text(strip=True)
            print(f"Calories: {_calories}")
#===========================================================================================================
        _image_container = soup.find('figure', class_='photo mntl-universal-image universal-image__container')
        if not _image_container:
            _image_container = soup.find('figure', class_=lambda x: x and 'photo mntl-universal-image universal-image__container' in x)

        _fileName = ""
        if _image_container:
            img_tag = _image_container.find('img')
            if img_tag and img_tag.has_attr('data-src'):
                img_url = img_tag['data-src']

                if "imagesvc.meredithcorp.io" in img_url:
                    base_url = urlsplit(img_url).query
                    url_param = base_url.split('&')[0]  
                    decoded_url = unquote(url_param.split('=')[1])  
                    img_url = decoded_url  

                img_extension = os.path.splitext(urlsplit(img_url).path)[1]
                if img_extension:
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        _fileName = convert_dishname_to_id(_title)
                        img_filename = f"assets/{_fileName}{img_extension}"
                        with open(img_filename, 'wb') as f:
                            f.write(img_response.content)
                        print(f"Image: {_fileName}.jpg")
                else:
                    print("Không thể xác định extension")
                    print("================================================================")
                    time.sleep(1)
                    return None
            else:
                print("Không tìm thấy URL ảnh trong thẻ img.")
                print("================================================================")
                time.sleep(1)
                return None
        else:
            print("Không tìm thấy ảnh trong class 'photo mntl-universal-image universal-image__container'.")
            print("================================================================")
            time.sleep(1)
            return None


#===========================================================================================================
        data = {
            "Image": [_fileName],
            "Food Name": [_title],
            "Summary": [_subheading],
            "Ingredients": [list_ingredients],
            "Calories": [_calories],
        }

        with open("output.csv", "a", encoding="utf-8") as file:
            file.write(f'\n{_fileName},{_title},"{_subheading}",{list_ingredients}, {_calories}')
        
        df = pd.DataFrame(data)
        print("================================================================")
        time.sleep(1)
        return df
    else:
        print("Lỗi khi tải trang.")
        print("================================================================")
        time.sleep(1)
        return None






# def crawl_sitemap(sitemap_url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     }
#     response = requests.get(sitemap_url, headers)
    
#     if response.status_code == 200:
#         tree = ET.ElementTree(ET.fromstring(response.content))
#         root = tree.getroot()

#         ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
#         urls = [url.find('sm:loc', ns).text for url in root.findall('sm:url', ns)]
#         return urls
#     else:
#         print("Không thể tải sitemap.")
#         return None


def save_urls_to_File(urls, file_name='urlsRecipe.txt'):
    with open(file_name, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")

def read_urls_from_file(file_name='urlsRecipe.txt'):
    crawled = []
    with open("crawled_urls.txt", 'r') as f:
        crawled = [line.strip() for line in f.readlines()]

    with open(file_name, 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip() not in crawled]
    return urls



def crawl_allRecipes_inSitemap(urls):

    results = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i, result in enumerate(executor.map(crawl_recipe, urls)):
            results.append(result)
            time.sleep(1)  

    valid_results = [df for df in results if df is not None]
    return pd.concat(valid_results, ignore_index=True)


def crawl_sitemap(sitemap_url):
    driver = get_selenium_driver()
    driver.get(sitemap_url)  
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()  
    urls = [loc.get_text() for loc in soup.find_all('loc')]
    return urls


def crawl_links():
    for i in range(1, 5):
        sitemap_url = f'https://www.allrecipes.com/sitemap_{i}.xml'
        urls = crawl_sitemap(sitemap_url)
        save_urls_to_File(urls, f"urlsRecipe_sitemap{i}.txt")
        print(f"Số lượng url: {len(urls)}")
        for url in urls:
            print(url)




# Chỉnh url_file thành file .txt chứa các url cần crawl

def main():
    url_file = r"links/urlsRecipe_sitemap1.txt"

    # Folder chứa thư mục ảnh
    img_folder = "assets"
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    if not os.path.exists("crawled_urls.txt"):
        f = open("crawled_urls.txt", "w", encoding="utf-8")

    if not os.path.exists("output.csv"):
        with open("output.csv", "w", encoding="utf-8") as file:
            file.write("Image,Food Name,Summary,Ingredients,Calories")

    _urls = read_urls_from_file(url_file)
    df_recipes = crawl_allRecipes_inSitemap(_urls)
    #df_recipes.to_csv('recipes.csv', index=False)
    #print(df_recipes)
    print(_urls)

if __name__ == '__main__':
    main()