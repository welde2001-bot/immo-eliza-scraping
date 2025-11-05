from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Setup Firefox WebDriver
# Make sure you have geckodriver installed and available in your PATH
service = Service()
driver = webdriver.Firefox(service=service)

# Open the property page
url = "https://immovlan.be/en/detail/villa/for-sale/9051/sint-denijs-westrem/rbu55821"
driver.get(url)
time.sleep(5)  # Wait for the page to fully load

# TERRACE: 1 = Yes, 0 = No, None if missing 
try:
    terrace_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Terrace')]/following-sibling::p").text
    terrace = 1 if "Yes" in terrace_text else 0
except:
    terrace = None

# GARDEN: 1 = Yes, 0 = No
try:
    garden_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Garden')]/following-sibling::p").text
    garden = 1 if "Yes" in garden_text else 0
except:
    garden = 0

# GARDEN AREA (m²): integer or None
try:
    garden_area_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Surface garden')]/following-sibling::p").text
    garden_area = int(garden_area_text.replace("m²", "").replace("m", "").strip())
except:
    garden_area = None

# NUMBER OF FACADES: integer or None 
try:
    facades_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Number of facades')]/following-sibling::p").text
    facades = int(facades_text)
except:
    facades = None

# SWIMMING POOL: 1 = Yes, 0 = No
try:
    pool_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Swimming pool')]/following-sibling::p").text
    swimming_pool = 1 if "Yes" in pool_text else 0
except:
    swimming_pool = 0

# STATE OF BUILDING: text or None
try:
    state = driver.find_element(By.XPATH, "//h4[contains(text(), 'State of the property')]/following-sibling::p").text
except:
    state = None

# BUILD YEAR: integer or None 
try:
    build_year_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Build Year')]/following-sibling::p").text
    build_year = int(build_year_text)
except:
    build_year = None

# NUMBER OF ROOMS: integer or None
try:
    number_rooms_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Number of bedrooms')]/following-sibling::p").text
    number_rooms = int(number_rooms_text)
except:
    number_rooms = None

# LIVING AREA (m²): integer or None
try:
    living_area_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Livable surface')]/following-sibling::p").text
    living_area = int(living_area_text.replace("m²", "").replace("m", "").strip())
except:
    living_area = None

# EQUIPPED KITCHEN: 1 = Yes, 0 = No, None if missing 
# EQUIPPED KITCHEN: 1 = yes, 0 = no, None if missing
try:
    kitchen_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Kitchen equipment')]/following-sibling::p").text
    if "equipped" in kitchen_text.lower():  # any text containing "equipped"
        equipped_kitchen = 1
    elif "not" in kitchen_text.lower():      # text containing "not"
        equipped_kitchen = 0
    else:
        equipped_kitchen = None
except:
    equipped_kitchen = None

# FURNISHED: 1 = Yes, 0 = No, None if missing
try:
    furnished_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Furnished')]/following-sibling::p").text
    if "yes" in furnished_text.lower():
        furnished = 1
    elif "no" in furnished_text.lower():
        furnished = 0
    else:
        furnished = None
except:
    furnished = None

# # OPEN FIRE: 1 = Yes, 0 = No, None if missing 
# try:
#     open_fire_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Open fire')]/following-sibling::p").text
#     if "Yes" in open_fire_text:
#         open_fire = 1
#     elif "No" in open_fire_text:
#         open_fire = 0
#     else:
#         open_fire = None
# except:
#     open_fire = None

# Print results 
print("Terrace:", terrace)
print("Garden presence:", garden)
print("Garden area:", garden_area)
print("Number of facades:", facades)
print("Swimming pool:", swimming_pool)
print("State of building:", state)
print("Build year:", build_year)
print("Number of rooms:", number_rooms)
print("Living area (m²):", living_area)
print("Equipped kitchen:", equipped_kitchen)
print("Furnished:", furnished)
#print("Open fire:", open_fire)

# Close browser 
driver.quit()
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
