from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def scrape_properties(urls, output_file="data/properties.csv"):
    """Scrape property details from a list of URLs."""
    options = Options()
    options.headless = True
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    gecko_path = r"C:\Users\geckodriver.exe"

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "url", "property_id", "property_type", "locality_name", "postal_code",
            "build_year", "state", "living_area", "furnished", "number_rooms",
            "equipped_kitchen", "terrace", "facades", "garden", "garden_area",
            "swimming_pool", "price"
        ])

        for url in urls:
            driver = None
            try:
                driver = webdriver.Firefox(service=Service(gecko_path), options=options)
                driver.get(url)
                print(url)

                try:
                    accept_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
                    )
                    accept_button.click()
                except:
                    pass

                try:
                    price = driver.find_element(By.CSS_SELECTOR, "span.detail__price").text
                except:
                    price = "None"

                row = [url, "None", "None", "None", "None",
                       "None", "None", "None", "None", "None",
                       "None", "None", "None", "None", "None", "None", price]
                writer.writerow(row)

            except Exception as e:
                print(f"Error loading {url}: {e}")
            finally:
                if driver:
                    driver.quit()

    print(f"Scraping complete. Saved to {output_file}")


def scrape_properties_from_file(input_file="data/urls.csv", output_file="data/properties.csv"):
    """Load URLs from CSV and scrape them."""
    urls = []
    with open(input_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "URL" in row and row["URL"].startswith("http"):
                urls.append(row["URL"])

    print(f"Loaded {len(urls)} URLs from {input_file}")
    scrape_properties(urls, output_file)


if __name__ == "__main__":
    scrape_properties_from_file()
