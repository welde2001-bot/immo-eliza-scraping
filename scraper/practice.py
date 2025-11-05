

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# URL to scrape
urls = [
    "https://immovlan.be/en/detail/villa/for-sale/9051/sint-denijs-westrem/rbu55821",
]

# Firefox options (headless)
options = Options()
options.add_argument("--headless")

# Loop through URLs
for url in urls:
    driver = None
    try:
        # Launch Firefox
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)


        try:
            terrace_tag = driver.find_element(By.CSS_SELECTOR, "h4:contains('Terrace') + p")
            terrace_text = terrace_tag.text.strip()
            terrace = 1 if "yes" in terrace_text.lower() else 0
        except:
            terrace = None 




        # GARDEN: 1 = Yes, 0 = No
        try:
            garden_blocks = driver.find_elements(By.CSS_SELECTOR, "div")
            garden = 0  # default
            for block in garden_blocks:
                try:
                    h4_text = block.find_element(By.CSS_SELECTOR, "h4").text.strip().lower()
                    if "garden" == h4_text:  # exact match for Garden
                        garden_text = block.find_element(By.CSS_SELECTOR, "p").text.strip()
                        garden = 1 if "yes" in garden_text.lower() else 0
                        break
                except:
                    continue
        except:
            garden = 0

            



            # GARDEN AREA (m²): integer or None
            try:
                garden_area = None
                for block in garden_blocks:
                    try:
                        h4_text = block.find_element(By.CSS_SELECTOR, "h4").text.strip().lower()
                        if "surface garden" in h4_text:
                            garden_area_text = block.find_element(By.CSS_SELECTOR, "p").text.strip()
                            garden_area = int(garden_area_text.replace("m²", "").replace("m", "").strip())
                            break
                    except:
                        continue
            except:
                garden_area = None

           

        # -----------------------
        # Extract property ID
        # -----------------------
        try:
            property_id = url.split('/')[-1]
        except:
            property_id = None

        # -----------------------
        # Extract postal code & locality
        # -----------------------
        try:
            city_tag = driver.find_element(By.CSS_SELECTOR, ".city-line")
            city_text = city_tag.text.strip()
            postal_code = city_text.split()[0]
            locality_name = " ".join(city_text.split()[1:])
        except:
            postal_code = None
            locality_name = None

        # -----------------------
        # Extract price
        # -----------------------
        try:
            price_tag = driver.find_element(By.CSS_SELECTOR, ".detail__header_price_data")
            price = price_tag.text.strip()
        except:
            price = None

        # -----------------------
        # Extract property type & subtype
        # -----------------------
        try:
            type_tag = driver.find_element(By.CSS_SELECTOR, ".detail__header_title_main")
            type_words = type_tag.text.strip().split()
            property_type = type_words[0]
            #subtype = " ".join(type_words[1:]) if len(type_words) > 1 else ""
        except:
            property_type = None
            #subtype = None
            

        # -----------------------
        # Print results
        # -----------------------
        print("Terrace:", terrace)
        print("Garden:", garden)
        print("Garden area (m²):", garden_area)
        
        print("Property ID:", property_id)
        print("Postal Code:", postal_code)
        print("Locality:", locality_name)
        print("Price:", price)
        print("Type:", property_type)
        #print("Subtype:", subtype)
        print("-" * 40)

    except:
        print("Error loading page:", url)
    finally:
        if driver:
            driver.quit()