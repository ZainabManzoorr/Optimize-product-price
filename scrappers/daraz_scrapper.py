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


def scrape_daraz_laptops(search_query="laptop", pages=3, output_file="daraz_laptops.csv"):
    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", output_file)

    # Setup Chrome options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_products = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        url = f"https://www.daraz.pk/catalog/?q={search_query}&page={page}"
        driver.get(url)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@title]"))
            )
        except:
            print(f"⚠️ No products found on page {page}")
            continue

        product_cards = driver.find_elements(By.XPATH, "//a[@title]")

        for card in product_cards:
            try:
                title = card.get_attribute("title")
                link = card.get_attribute("href")
            except:
                title, link = None, None

            
            parent = card.find_element(By.XPATH, "./..")

            try:
                price = parent.find_element(By.XPATH, ".//span[@class='currency--GVKjl']").text.strip()
            except:
                price = None

            try:
                discount_price = parent.find_element(By.XPATH, ".//span[@class='price--NVB62']").text.strip()
            except:
                discount_price = None

            try:
                rating = parent.find_element(By.XPATH, ".//span[@class='rating']").text.strip()
            except:
                rating = None

            try:
                reviews = parent.find_element(By.XPATH, ".//span[contains(@class,'rating__review')]").text.strip()
            except:
                reviews = None

            if title:
                all_products.append({
                    "Title": title,
                    "Link": link,
                    "Price": price,
                    "Discount Price": discount_price,
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
        print("No data scraped")

    return df


if __name__ == "__main__":
    df = scrape_daraz_laptops(pages=3)
    print(df.head())
