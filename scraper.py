from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# TERRACE: 1 = Yes, 0 = No, None if missing
try:
    terrace_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Terrace')]/following-sibling::p").text
    terrace = 1 if "Yes" in terrace_text else 0
except:
    terrace = None

# GARDEN PRESENCE: 1 = Yes, 0 = No
try:
    garden_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Garden')]/following-sibling::p").text
    garden = 1 if "Yes" in garden_text else 0
except:
    garden = 0

# GARDEN AREA (m²): integer or None
try:
    garden_area_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Surface garden')]/following-sibling::p").text
    garden_area = int(garden_area_text.replace("m²", "").strip())
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


print("Terrace:", terrace)
print("Garden presence:", garden)
print("Garden area:", garden_area)
print("Number of facades:", facades)
print("Swimming pool:", swimming_pool)
print("State of building:", state)
print("Build year:", build_year)