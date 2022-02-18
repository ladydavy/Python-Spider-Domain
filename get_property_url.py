import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()

file_path = 'postcode_suburb_new_1497.csv'
pc_sb_list = pd.read_csv(file_path)

postcode_list = []
suburb_list = []
property_list = []
# page_list = []

for index, row in pc_sb_list.iterrows():
    postcode = row['postcode']
    suburb = row['suburb']
    post_sub = row['post_sub']

    url = "https://www.domain.com.au/sold-listings/" + post_sub + "/"

    print(postcode,suburb,post_sub,url)

    page_number = 1
    while True:
        print(page_number)
        page_url = url + "?page=" + str(page_number)
        driver.get(page_url)
        stop = -1
        sold_tags = driver.find_elements(By.CLASS_NAME, "css-1nj9ymt")
        if not sold_tags:
            break
        for tag in sold_tags:
            time_text = tag.text
            if "2020" in time_text or "2019" in time_text or "2018" in time_text or "2017" in time_text:
                stop = 1
                break

        links = driver.find_elements(By.CLASS_NAME, "address.is-two-lines.css-1y2bib4")
        for link in links:
            property_url = link.get_attribute('href')
            postcode_list.append(postcode)
            suburb_list.append(suburb)
            property_list.append(property_url)
            print(postcode,suburb,property_url)

        if stop == 1:
            break
        page_number = page_number + 1
        if page_number >50:
            break

columns_name = ['postcode','suburb','property']
df = pd.DataFrame(list(zip(postcode_list,suburb_list,property_list)),columns = columns_name)
# df = pd.DataFrame(list(zip(postcode_list,suburb_list)))

df.to_csv('postcode_suburb_property_1497.csv')