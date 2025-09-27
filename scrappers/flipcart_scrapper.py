import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_flipkart_laptops(search_query="laptop", pages=3, output_file="flipkart_laptops.csv"):
    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", output_file)

    # Setup Chrome options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_products = []

    for page in range(1, pages + 1):
        print(f"Scraping Flipkart page {page}...")
        url = f"https://www.flipkart.com/search?q={search_query}&page={page}"
        driver.get(url)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'_1AtVbE')]"))
            )
        except:
            print(f"No products found on Flipkart page {page}")
            continue

        product_cards = driver.find_elements(By.XPATH, "//div[contains(@class,'_1AtVbE')]")

        for card in product_cards:
            try:
    
                try:
                    title = card.find_element(By.XPATH, ".//div[@class='KzDlHZ']").text.strip()
                except:
                    title = None
            except:
                title = None

            try:
                price = card.find_element(By.XPATH, ".//div[@class='Nx9bqj _4b5DiR']").text.strip()
            except:
                price = None

            try:
                rating = card.find_element(By.XPATH, ".//div[@class='XQDdHH']").text.strip()
            except:
                rating = None

            try:
                reviews = card.find_element(By.XPATH, ".//span[@class='Wphh3N']").text.strip()
            except:
                reviews = None

            if title:
                all_products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Reviews": reviews
                })

        time.sleep(2)

    driver.quit()

    df = pd.DataFrame(all_products)
    if not df.empty:
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Scraping complete. Saved to {output_path}")
    else:
        print("No data scraped from Flipkart")

    return df


if __name__ == "__main__":
    df = scrape_flipkart_laptops(pages=3)
    print(df.head())
