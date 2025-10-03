import time
import random
from plyer import notification
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def fetch_products(driver):
    url = "https://www.jbhifi.com.au/search?query=pokemon%20tcg"
    driver.get(url)
    time.sleep(4)

    cards = driver.find_elements(By.CLASS_NAME, "ProductCard_content")
    results = []

    for card in cards:
        try:
            title = card.find_element(By.TAG_NAME, "img").get_attribute("alt")
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        except Exception:
            continue

        try:
            price = card.find_element(By.CLASS_NAME, "BasePrice").text
        except:
            price = "No price listed"

        results.append({
            "title": title.strip(),
            "price": price.strip(),
            "link": link.strip()
        })

    print("\n📦 Product titles fetched:")
    for p in results:
        print(" -", p["title"])

    return results

def show_notification(term):
    notification.notify(
        title=f"{term} is on JB Hi-Fi!",
        message=f"A Pokémon product matching '{term}' was just listed.",
        timeout=10,
        app_name="JB Hi-Fi Watcher"
    )

def main():
    search_terms = ["Prismatic", "151", "Bundle", "Elite"]#, "Destined Rivals"]
    first_run = True
    driver = setup_driver()

    while True:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔍 Checking for listings matching: {', '.join(search_terms)}")

        try:
            products = fetch_products(driver)
        except Exception as e:
            print(f"❌ Error: {e}")
            products = []

        found_terms = set()

        for product in products:
            title = product["title"]
            for term in search_terms:
                if term.lower() in title.lower():
                    if term not in found_terms:
                        found_terms.add(term)
                        print(f"🔔 Match: {title}")
                        show_notification(term)

        if not found_terms:
            print("No matching items found.")

        wait_time = 5 if first_run else random.randint(10,30)
        first_run = False
        print(f"⏳ Waiting {wait_time} seconds before next check...\n")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
