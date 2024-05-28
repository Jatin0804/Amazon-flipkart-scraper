import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)


def main():

    records = []
    url = "https://www.indexmundi.com/commodities/"

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    parent_commodities = soup.find('table', 'tblData')
    all_commodities = parent_commodities.find_all('tr')

    
    for item in all_commodities:
        try:
            temp = []
            
            a_tag = item.find('td').a
            link = a_tag.get('href')

            all_values = item.find_all('td')
            for i in all_values:
                temp.append(i.text)

            link = url + link
            temp.append(link)
            records.append(temp)
        except:
            continue

    # Close the driver
    driver.quit()

    
    # Write records to CSV
    with open(f'all_commodities.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Commodity Name', 'Monthly Avg', '1 Month Change', '12 Month Change', 'Year to Date Change', 'URL'])
        writer.writerows(records)


    # Write records to JSON
    json_records = [{key: value for key, value in zip(['Commodity Name', 'Monthly Avg', '1 Month Change', '12 Month Change', 'Year to Date Change', 'URL'], record)} for record in records]
    with open(f'all_commodities.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_records, json_file, ensure_ascii=False, indent=4)

main()