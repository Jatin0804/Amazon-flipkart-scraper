import json
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_url(search_term):
    template = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url += '&page={}'
    return url

def extract_record(item):
    # Extract product information from search result item
    a_tag = item.div.a
    # description = a_tag.text.strip()
    url = 'https://www.flipkart.com/' + a_tag.get('href')

    try:
        description = item.find('div', 'KzDlHZ').text
    except AttributeError:
        description = ""

    # Extract price, rating, review count
    previous_price = ""
    try:
        price_parent = item.find('div', 'hl05eU')
        price = price_parent.find('div', 'Nx9bqj _4b5DiR').text
    except AttributeError:
        price = None

    try:
        rating = item.find('div', 'XQDdHH').text
        rating_count_parent = item.find('span', {'class': 'Wphh3N'})
        rating_count = rating_count_parent.span.span.text
    except AttributeError:
        rating = 'No reviews'
        rating_count = '0'

    percent_discount = ""
    if previous_price:
        # Calculate percent discount if there's a previous price
        percent_discount = round(
            ((float(price[1:].replace(",", "")) - float(previous_price[1:].replace(",", ""))) /
            float(previous_price[1:].replace(",", ""))) * 100, 2
        )
        percent_discount = f"{percent_discount}%"

    # Return extracted record
    result = {'Description': description, 'Price': price, 'Rating': rating, 'Rating Count': rating_count, 'URL': url}
    return result

def main(search_term):
    # Set up Chrome options and Service
    chrome_options = Options()
    # Double backslashes or raw strings for Windows paths

    driver = webdriver.Chrome(options=chrome_options)

    records = []
    url = get_url(search_term)

    for page in range(1, 10):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', '_75nlfW')
        # records.append(results)

        for item in results:
            record = extract_record(item)
            if record:  # Only append valid records
                records.append(record)

    # Close the driver
    driver.quit()

    # Write records to JSON
    with open(f'JSON_files/{search_term}_flipkart.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

# Ask for search term and run the scraper
search_term = input("Search term: ")
main(search_term)
# main("mobiles")
