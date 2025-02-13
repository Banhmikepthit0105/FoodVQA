
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# !!!IMPORTANT: Path to your ChromeDriver
chrome_driver_path = "C:/chromedriver-win64/chromedriver.exe"   # Replace with your path

def crawl_recipe(url, file_name="recipe_page", driver_path = "C:/chromedriver-win64/chromedriver.exe" ):

    # Set up Selenium options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920x1080")
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    try:
        print("Opening URL...")
        driver.get(url)
        print("URL loaded successfully.")

        # Extract page source
        page_source = driver.page_source
        print("Page source extracted.")
        

        driver.quit()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        print("Page parsed with BeautifulSoup.")
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(soup.prettify())


    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
