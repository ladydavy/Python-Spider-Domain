import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
from csv import writer
driver = webdriver.Chrome()

old_done_list_path = 'done_list.csv'
old_done_list = pd.read_csv(old_done_list_path)['property_url'].values.tolist()

# new_done_list = []

file_path = 'postcode_suburb_property_1497_unique.csv'
url_list = pd.read_csv(file_path)

# list_postcode = []
# list_suburb = []
# list_url = []
# list_sold_time = []
# list_price = []
# list_location = []
# list_beds = []
# list_baths = []
# list_parking = []
# list_area = []
# list_type = []
# list_features = []
# list_description = []

flag = 0
# time_start = time.time()
for index, row in url_list.iterrows():
    # property_url = "https://www.domain.com.au/14-mcdonough-lane-vermont-vic-3133-2016840264"
    postcode = row['postcode']
    suburb = row['suburb']
    property_url = row['property']

    if property_url in old_done_list:
        continue

    driver.get(property_url)

    # time
    try:
        sold_time = driver.find_element(By.CLASS_NAME, "css-h9g9i3").text
    except NoSuchElementException:
        sold_time = "None"


    if "2021" not in sold_time:
        new_line = [property_url]
        with open('done_list.csv', 'a', newline='', encoding='utf-8') as f_object:
            # Pass the CSV  file object to the writer() function
            writer_object = writer(f_object)
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(new_line)
            # Close the file object
            f_object.close()
        continue

    # new_done_list.append(property_url)

    # list_postcode.append(postcode)
    # list_suburb.append(suburb)
    # list_url.append(property_url)
    # list_sold_time.append(sold_time)
    print(property_url)
    # print(sold_time)
    # price
    try:
        price = driver.find_element(By.CLASS_NAME, "css-1texeil").text
    except NoSuchElementException:
        price = "None"
    # list_price.append(price)
    # print(price)
    # location
    try:
        location = driver.find_element(By.CLASS_NAME, "css-164r41r").text
    except NoSuchElementException:
        location = "None"
    # list_location.append(location)
    # print(location)
    try:
        basic_features = driver.find_elements(By.CLASS_NAME, "css-1ie6g1l")
    except NoSuchElementException:
        pass
    # basic features: beds, baths, parking
    # beds = re.findall(r"\d+\.?\d*",basic_features[0].text)[0]
    # baths = re.findall(r"\d+\.?\d*",basic_features[1].text)[0]
    # parking = re.findall(r"\d+\.?\d*",basic_features[2].text)[0]
    beds = "None"
    baths = "None"
    parking = "None"
    area = "None"
    if basic_features:
        for feature in basic_features:
            if "Bed" in feature.text:
                beds = re.findall(r"\d+\.?\d*", feature.text)[0]
            elif "Bath" in feature.text:
                baths = re.findall(r"\d+\.?\d*", feature.text)[0]
            elif "Parking" in feature.text:
                parking = re.findall(r"\d+\.?\d*", feature.text)[0]
            elif "m" in feature.text or "ha" in feature.text:
                area = feature.text

    # list_beds.append(beds)
    # list_baths.append(baths)
    # list_parking.append(parking)
    # list_area.append(area)
    # print(beds, baths, parking, area)
    # property type

    try:
        typ = driver.find_element(By.CLASS_NAME, "css-1uvlh9e").text
    except NoSuchElementException:
        typ = "None"
    # list_type.append(typ)
    # print(type)
    # other features
    try:
        view_all_features = driver.find_element(By.CLASS_NAME,"css-1yiw84b")
        driver.execute_script("arguments[0].click();", view_all_features)
    except NoSuchElementException:
        pass

    try:
        other_features = driver.find_element(By.NAME, "property-features").text
    except NoSuchElementException:
        other_features = "None"
    # list_features.append(other_features)
    # print(other_features)
    # property description
    try:
        read_more = driver.find_element(By.CLASS_NAME,"css-1pn4141")
        driver.execute_script("arguments[0].click();", read_more)
    except NoSuchElementException:
        pass

    try:
        description = driver.find_element(By.NAME, "listing-details__description").text
    except NoSuchElementException:
        description = "None"
    # list_description.append(description)
    # print(description)

    new_line = [postcode,suburb,property_url,sold_time,price,location,beds,baths,parking,area,typ,other_features,description]
    with open('property_info.csv', 'a', newline='',encoding='utf-8') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(new_line)
        # Close the file object
        f_object.close()

    # flag = flag + 1
    # if flag % 2 == 0:
    #     columns_name = ['postcode','suburb','property_url','sold_time','price','address','#beds','#baths','#parking','area','type','features','description']
    #     df = pd.DataFrame(list(zip(list_postcode,list_suburb,list_url,list_sold_time,list_price,list_location,list_beds,list_baths,list_parking,list_area, list_type,list_features,list_description)),columns = columns_name)
    #     output_file = 'C:/Monash University/Guanliang/property_info_' + str(flag) + '.csv'
    #     df.to_csv(output_file)
    new_line = [property_url]
    with open('done_list.csv', 'a', newline='',encoding='utf-8') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(new_line)
        # Close the file object
        f_object.close()

    flag = flag + 1
    print(flag, "Done!")
        # list_postcode.clear()
        # list_suburb.clear()
        # list_url.clear()
        # list_sold_time.clear()
        # list_price.clear()
        # list_location.clear()
        # list_beds.clear()
        # list_baths.clear()
        # list_parking.clear()
        # list_area.clear()
        # list_type.clear()
        # list_features.clear()
        # list_description.clear()
        # time_end = time.time()
        # print("output: ", flag, 'time cost: ', time_end-time_start,'s')
        # time_start = time.time()

# columns_name = ['postcode','suburb','property_url','sold_time','price','address','#beds','#baths','#parking','area','type','features','description']
# df = pd.DataFrame(list(zip(list_postcode,list_suburb,list_url,list_sold_time,list_price,list_location,list_beds,list_baths,list_parking,list_area, list_type,list_features,list_description)),columns = columns_name)
# output_file = 'C:/Monash University/Guanliang/property_info_' + str(flag) + '.csv'
# df.to_csv(output_file)
