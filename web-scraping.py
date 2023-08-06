from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
import time
import json
import csv
import os

# Create webdriver object
EXECUTABLE_PATH = r"C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=EXECUTABLE_PATH)

# If the csv does not exist
if not os.path.exists("bekasi-house.csv"):
    # Create columns
    csvfile = open('bekasi-house.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(["id", "url", "price", "description"])
else:
    csvfile = open('bekasi-house.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)

# Specify the starting page number
START_PAGE = 1

# Specify the max page number
MAX_PAGE = 50

for page_num in range(START_PAGE, MAX_PAGE+1):
    endpoint = f"https://www.rumah123.com/jual/bekasi/rumah/?page={page_num}"

    driver.get(endpoint)
    time.sleep(1)
    house_tags = driver.find_elements(by=By.CSS_SELECTOR, value=".card-featured__middle-section["
                                                                "data-test-id='card-middle-section']")

    # Lists containing data for each page
    house_ids = []
    url_links = []
    prices = []
    inputs = []

    for tag in house_tags:

        # Price
        price = tag.find_element(by=By.CLASS_NAME, value="card-featured__middle-section__price").text.split("\n")[0]
        prices.append(price)

        ads_tag = tag.find_element(by=By.TAG_NAME, value="a")

        # URL Link and ID
        url_link = ads_tag.get_attribute("href")
        house_id = url_link.split("/")[-2]

        url_links.append(url_link)
        house_ids.append(house_id)

    print(f"Number of data in Page {page_num}: {len(url_links)}")

    # Go to each links appended to url_links
    for url_link in url_links:
        driver.get(url_link)
        time.sleep(1)

        # Inputs
        body_tag = driver.find_element(by=By.TAG_NAME, value="body")

        # See more details on house ads
        see_more = driver.find_element(by=By.XPATH, value='//*[@id="property-information"]/div[1]/div/div[2]')
        driver.execute_script("arguments[0].scrollIntoView();", see_more)
        time.sleep(1)

        try:
            driver.execute_script("arguments[0].click();", see_more)
            time.sleep(1)
        except StaleElementReferenceException:
            # See the block
            details_tag = driver.find_element(by=By.CSS_SELECTOR, value="div.ui-listing-specification__badge-wrapper")
            details = details_tag.find_elements(by=By.CSS_SELECTOR, value="div.ui-listing-specification__badge")
        except WebDriverException:
            # See the block
            details_tag = driver.find_element(by=By.CSS_SELECTOR, value="div.ui-listing-specification__badge-wrapper")
            details = details_tag.find_elements(by=By.CSS_SELECTOR, value="div.ui-listing-specification__badge")
        else:
            details = driver.find_elements(by=By.CLASS_NAME, value="ui-listing-specification__table--row")

        # Get the dictionary by containing its contents to string first
        details_str = '{'
        for detail in details:
            new_item = detail.text.split("\n")[0]
            new_value = detail.text.split("\n")[1]
            new_data = f'"{new_item}": "{new_value}", '
            details_str += new_data
        details_str += '}'

        # Convert the string to dictionary
        details_str = details_str.replace(", }", "}")
        details_dict = json.loads(details_str)
        inputs.append(details_dict)

    # Add Rows
    for i in range(len(inputs)):
        new_data = [house_ids[i], url_links[i], prices[i], inputs[i]]
        writer.writerow(new_data)

    print(f"Page {page_num}: Done \n")

csvfile.close()