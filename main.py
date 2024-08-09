from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


import csv

# Function to save data to CSV file
def save_to_csv(data, filename):
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Start the browser
service = Service(executable_path='/snap/bin/geckodriver')
browser = webdriver.Firefox(service=service)

def extract_data(browser):
    data_list = []
    try:
        parent_div = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "zero-results-similar-wrap")))
        project_wrappers = parent_div.find_elements(By.CLASS_NAME, "cardLayout")
        for project_wrapper in project_wrappers:
            project_name = project_wrapper.find_element(By.CLASS_NAME, "projName").text
            project_price = project_wrapper.find_element(By.CLASS_NAME, "price").text
            builtup_area = project_wrapper.find_element(By.CLASS_NAME, "size").text
            rate_per_sqft = project_wrapper.find_element(By.CLASS_NAME, "lbl").text
            bhk = project_wrapper.find_element(By.CLASS_NAME, "val").text
            location = project_wrapper.find_element(By.CLASS_NAME, "locName").text
            construction_details_elem = project_wrapper.find_elements(By.CLASS_NAME, "val")[-1]
            construction_details = construction_details_elem.text if construction_details_elem else "N/A"
            builder_name = project_wrapper.find_element(By.CLASS_NAME, "seller-name").text
            data_list.append({"Project Name": project_name,"Project Price": project_price,"Builtup Area": builtup_area,"Rate per SQft":rate_per_sqft, "BHK":bhk,"Location":location,"Construction Details":construction_details,"Builder Name":builder_name})
    except Exception as e:
        print("Error scraping data:", e)
    return data_list

base_url = 'https://www.makaan.com/mumbai-residential-property/buy-property-in-mumbai-city?page='
page_count = 1000
all_data = []

# Loop through each page
for page in range(1, page_count + 1):
    url = base_url + str(page)
    browser.get(url)
    # Add a delay to ensure page loads completely
    time.sleep(5)
    page_data = extract_data(browser)
    print(f"Page {page} Data:")
    for project in page_data:
        print(project)
    all_data.extend(page_data)

browser.quit()

# Write all_data to CSV file
save_to_csv(all_data, 'data.csv')

print("-- done --")