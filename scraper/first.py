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