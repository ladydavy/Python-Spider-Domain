import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()

url = "https://postcodes-australia.com/state-postcodes/vic"


postcode_list = []
suburb_list = []
pc_sb_list = []

driver.get(url)

pc_list = driver.find_element(By.CLASS_NAME, "pclist").find_elements(By.TAG_NAME, "li")
for li in pc_list:
    if not any(map(str.isdigit, li.text)):
        continue
    # print(list.text)
    split_list = li.text.split("\n")
    postcode = split_list[0]
    # if postcode == "8873":
    split_list.pop(0)
    for suburb in split_list:
        if not suburb:
            break
        postcode_list.append(postcode)
        suburb_list.append(suburb)
        print(postcode, suburb)
        pc_sb = suburb.lower().replace(" ","-") + "-vic-" + postcode
        print(pc_sb)
        pc_sb_list.append(pc_sb)


columns_name = ['postcode','suburb','post_sub']
df = pd.DataFrame(list(zip(postcode_list,suburb_list,pc_sb_list)),columns = columns_name)
# df = pd.DataFrame(list(zip(postcode_list,suburb_list)))

df.to_csv('C:/Monash University/postcode_suburb_new.csv')