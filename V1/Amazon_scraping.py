import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_url(search_term):
    template = 'https://www.amazon.in/s?k={}'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url += '&page={}'
    return url

def extract_record(item):
    # Extract product information from search result item
    a_tag = item.h2.a
    description = a_tag.text.strip()
    url = 'https://www.amazon.in' + a_tag.get('href')

    try:
        sponsored = item.find('span', 'a-color-base').text
    except AttributeError:
        sponsored = ""

    # Extract price, rating, review count
    previous_price = ""
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        price = None

    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        rating = 'No reviews'
        review_count = '0'

    percent_discount = ""
    if previous_price:
        # Calculate percent discount if there's a previous price
        percent_discount = round(
            ((float(price[1:].replace(",", "")) - float(previous_price[1:].replace(",", ""))) /
            float(previous_price[1:].replace(",", ""))) * 100, 2
        )
        percent_discount = f"{percent_discount}%"

    # Return extracted record
    result = (description, price, rating, review_count, url)
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
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:  # Only append valid records
                records.append(record)

    # Close the driver
    driver.quit()

    # Write records to CSV
    with open(f'files/{search_term}_amazon.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'URL'])
        writer.writerows(records)

# Ask for search term and run the scraper
search_term = input("Search term: ")
main(search_term)
