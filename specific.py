from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import json
import time
import csv

url = 'https://www.duvalacura.com' 

service  = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service = service, options = options)

driver.get(url)

new_acuras = driver.find_elements(By.TAG_NAME,'a')

search_text = "Shop New"
search_text_7 = "Shop Pre-Owned"

for new_acura in new_acuras:
    if search_text in new_acura.text:
        print(new_acura.text," ::::: ", new_acura.get_attribute("href"))  
        break

for new_acura in new_acuras:    
    if search_text_7 in new_acura.text:
        print(new_acura.text," ::::: ", new_acura.get_attribute("href"))
        

with open('Links.csv', mode = 'w') as csvfile:
        for new_acura in new_acuras:
            if search_text in new_acura.text:
                Fieldnames = ["Shop New Acura : " , "Link"]
                writer = csv.DictWriter(csvfile, fieldnames = Fieldnames)
                writer.writeheader()
                writer.writerow({"Shop New Acura : " : new_acura.text, "Link" : new_acura.get_attribute("href")})
            if search_text_7 in new_acura.text:
                Fieldnames = ["Shop Pre-Owned Acura : ","Link"]
                writer = csv.DictWriter(csvfile, fieldnames = Fieldnames)
                writer.writeheader()
                writer.writerow({"Shop Pre-Owned Acura : " : new_acura.text, "Link" : new_acura.get_attribute("href")})

newc = driver.find_element(By.LINK_TEXT, 'Shop New')
newc.click()

wait = WebDriverWait(driver, 10)
wait.until(EC.url_contains('https://www.duvalacura.com/new-inventory/index.htm')) 

car_links = driver.find_elements(By.XPATH, '//a[span[@class="ddc-font-size-small"]]')

print(":::::::::::::::::::")
    
with open('Links.csv', mode = 'a') as csvfile:
        Fieldnames = ["New Cars' Names", "Links For New Cars"]
        writer = csv.DictWriter(csvfile, fieldnames = Fieldnames)
        for car_link in car_links:
            writer.writeheader()
            writer.writerow({"New Cars' Names" : car_link.text, "Links For New Cars" : car_link.get_attribute("href")})

extracted_data_list = []

for car_link in car_links:
    link_href = car_link.get_attribute('href')
    driver.execute_script('window.open("'+link_href+'", "_blank");')
    driver.switch_to.window(driver.window_handles[-1])  # Creates new tab for further code execution.
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains(link_href))
    # Extracting data
    details1 = driver.find_element(By.CLASS_NAME, 'col-xs-6')
    det_attributes = details1.find_elements(By.TAG_NAME, 'dt')
    det_values = details1.find_elements(By.TAG_NAME, 'dd')
    car_details ={}
    for det_attribute, det_value in zip(det_attributes, det_values):
        car_details[det_attribute.text] = det_value.text
    extracted_data_list.append(car_details)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

json_file_path = 'extracted_data.json'

with open(json_file_path, 'w') as json_file:
    json.dump(extracted_data_list, json_file, indent=4)

print("Data saved to", json_file_path)

time.sleep(60)
driver.quit()
