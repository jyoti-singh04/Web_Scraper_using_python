import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np

# Set up the Chrome driver
service = Service('"D:\software\Driver\chromedriver.exe"')  # Replace 'path_to_chromedriver' with the actual path to chromedriver executable
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode (without opening a browser window)
driver = webdriver.Chrome(service=service, options=options)

# Create the URL object
url = 'https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787'

# Load the URL in the browser
driver.get(url)

# Wait for the table to load (adjust the sleep time if needed)
time.sleep(5)

# Find the table element
table = driver.find_element(By.ID, 'table_id')

# Obtain every title of columns with tag <th>
headers = [header.text.strip() for header in table.find_elements(By.TAG_NAME, 'th')]


# Create a DataFrame
mydata = pd.DataFrame(columns=headers)

# Find the rows of the table
rows = table.find_elements(By.TAG_NAME, 'tr')
for row in rows[2:11]:  # Get data for first 5 rows
    try:
        row_data = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')]
        if len(row_data) == len(headers):
            mydata.loc[len(mydata)] = row_data
        else:
            row_data += [np.nan] * (len(headers) - len(row_data))
            mydata.loc[len(mydata)] = row_data
    except ValueError:
        continue


# Export to csv
mydata.to_csv('webData.csv', index=False)
# Try to read csv
mydata2 = pd.read_csv('webData.csv')

# Close the browser
driver.quit()
