from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
import threading


def handle_cookies(driver):
    """Accept cookie popups if they appear."""
    selectors = [
        "#onetrust-accept-btn-handler",
        "#didomi-notice-agree-button",
        "button[aria-label='Accept all']",
    ]
    for selector in selectors:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            ).click()
            return
        except Exception:
            continue


def scrape_province(province_slug, province_name, results, lock, max_pages=5):
    """Scrape property URLs for one province."""
    options = Options()
    options.headless = True
    gecko_path = r"C:/Users/geckodriver.exe"
    driver = webdriver.Firefox(service=Service(gecko_path), options=options)

    try:
        for page in range(1, max_pages + 1):
            url = (
                f"https://immovlan.be/en/real-estate?"
                f"transactiontypes=for-sale&propertytypes=house,apartment"
                f"&provinces={province_slug}&page={page}&noindex=1"
            )
            driver.get(url)
            handle_cookies(driver)
            time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "article.list-view-item h2.card-title a")
                    )
                )
            except TimeoutException:
                continue

            links = driver.find_elements(By.CSS_SELECTOR, "article.list-view-item h2.card-title a")
            page_urls = {link.get_attribute("href").split("?")[0] for link in links if link.get_attribute("href")}

            with lock:
                results.update(page_urls)

            print(f"{province_name} - Page {page}: {len(page_urls)} URLs")

    finally:
        driver.quit()


def collect_urls(output_file="data/raw/urls.csv", max_pages=10):
    """Scrape property URLs for all provinces."""
    provinces = {
        "Flemish Brabant": "flemish-brabant",
        "Walloon Brabant": "walloon-brabant",
        "East Flanders": "east-flanders",
        "West Flanders": "west-flanders",
        "Hainaut": "hainaut",
        "Liège": "liege",
        "Limburg": "limburg",
        "Namur": "namur",
        "Antwerpen": "antwerpen",
        "Brussels": "brussel",
    }

    results = set()
    lock = threading.Lock()
    threads = []
    start_time = time.time()

    for name, slug in provinces.items():
        t = threading.Thread(target=scrape_province, args=(slug, name, results, lock, max_pages))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL"])
        for url in sorted(results):
            writer.writerow([url])

    print(f"Saved {len(results)} property URLs to {output_file}")
    print(f"Time taken: {time.time() - start_time:.2f} sec")


if __name__ == "__main__":
    collect_urls()
