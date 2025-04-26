import json
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

from requests_html import HTMLSession

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.5',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
           'X-Requested-With': 'XMLHttpRequest'}


# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
#
# driver = webdriver.Chrome(chrome_options=options)
# loginURL = "http://www.fantasysiteiamusing.com/login"
# url = "http://www.fantasysiteiamusing.com/"
#
# driver.get(loginURL)
# html = driver.page_source
#
# usernameField = driver.find_element_by_xpath('/html/body/div[3]/form[1]/div[2]/div/input')
# passwordField = driver.find_element_by_xpath('/html/body/div[3]/form[1]/div[3]/div/input')
# loginButton = driver.find_element_by_xpath('/html/body/div[3]/form[1]/div[4]/button')
#
# usernameField.send_keys(user)
# passwordField.send_keys(
# pass)
#
# loginButton.click()
# time.sleep(5)
# driver.get(url)
# time.sleep(5)

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
#
# driver = webdriver.Chrome(options)
# url = "https://www.finra.org/finra-data/fixed-income/corp-and-agency"
#
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })
# driver.execute_cdp_cmd("Network.enable", {})
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
# wait = WebDriverWait(driver, 30)
# driver.get(url)
# time.sleep(5)
# # html = driver.page_source
# #table = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ng-containter')))
# # for tab in table:
# #     print(tab.text)
#
# elem = driver.find_element(By.NAME, "ng-containter")
# print(elem)

# response = requests.get(url="https://www.finra.org/finra-data/fixed-income/corp-and-agency", headers=headers)
# soup = BeautifulSoup(response.content, 'html.parser')
#soup = BeautifulSoup(html, 'html.parser')
#elms = soup.find_all("div", attrs={'role': 'row'})
#print(elms)

# PYPPETEER_CHROMIUM_REVISION = '1263111'
# session = HTMLSession()
# url = "https://www.finra.org/finra-data/fixed-income/corp-and-agency"
# response = session.get(url)
# # response.html.render()
# response.html.render(sleep = 6, keep_page = True, scrolldown = True)
# print(response.html.html)
# soup = BeautifulSoup(response.html.html, 'html.parser')
# elms = soup.find_all("div", attrs={'role': 'row'})
# response.close()
# session.close()
# print(soup)

# This script does the following:
#
# Sets up a headless Chrome browser using Selenium.
# Navigates to the specified FINRA page.
# Waits for the grid to load.
# Implements a function to scrape visible rows in the grid.
# Continuously scrolls the grid and scrapes data until no new rows are loaded.
# Saves the scraped data to a CSV file.
#
# To use this script, you'll need to:
#
# Install the required packages: selenium and pandas.
# Download the appropriate ChromeDriver for your Chrome version and update the path in the script.
# Run the script.
#
# Please note:
#
# Web scraping may be against the terms of service of some websites. Always check and comply with the website's robots.txt file and terms of service.
# This script assumes a certain structure of the grid. If the website changes, you may need to update the selectors.
# The script may take some time to run as it needs to scroll through all the data.
# You might need to adjust the wait times depending on your internet speed and the website's responsiveness.

# To scrape data from an Angular grid on a webpage, we'll need to use a tool that can render JavaScript,
# as the content is likely dynamically loaded. Selenium is a good choice for this task.
# Here's a Python script that uses Selenium to scrape the data from the Angular grid on the FINRA page you specified:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Set up the Chrome driver (make sure you have chromedriver installed and in PATH)
service = Service('F:/chromedriver-126/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)

# Navigate to the page
url = "https://www.finra.org/finra-data/fixed-income/corp-and-agency"
driver.get(url)

# Wait for the grid to load
wait = WebDriverWait(driver, 10)
grid = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ag-center-cols-container")))


# Function to scrape visible rows
def scrape_visible_rows():
    # rows = driver.find_elements(By.CSS_SELECTOR, ".ag-center-cols-container .ag-row")
    rows = driver.find_elements(By.CSS_SELECTOR, ".ag-center-cols-container .ag-row ag-row-no-focus ag-row-odd ag-row-level-0 ag-row-group-contracted ag-row-position-absolute")
    data = []
    for row in rows:
        # cells = row.find_elements(By.CSS_SELECTOR, ".ag-cell")
        cells = row.find_elements(By.CSS_SELECTOR, ".ag-cell ag-cell-not-inline-editing ag-cell-auto-height ag-cell-value")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
    return data


# Scrape data
all_data = []
last_row_count = 0

while True:
    # Scrape visible rows
    data = scrape_visible_rows()
    all_data.extend(data)

    # Check if we've reached the end
    if len(all_data) == last_row_count:
        break

    last_row_count = len(all_data)

    # Scroll to the bottom of the grid
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", grid)
    time.sleep(1)  # Wait for new data to load

# Close the browser
driver.quit()

# Create a DataFrame
columns = ["CUSIP", "Issuer Name", "Coupon", "Maturity", "Last Update Date"]
df = pd.DataFrame(all_data, columns=columns)

# Save to CSV
df.to_csv("finra_corp_and_agency_data.csv", index=False)

print(f"Scraped {len(df)} rows of data and saved to finra_corp_and_agency_data.csv")
