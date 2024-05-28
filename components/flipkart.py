from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

def get_url(search_term):
    template = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url += '&page={}'
    return url

def extract_record_flipkart(item):
    # Extract product information from search result item
    a_tag = item.div.a
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


    # Return extracted record
    result = (description, price, rating, rating_count, url)
    return result

def main(search_term):

    records = []
    url = get_url(search_term)

    for page in range(1, 10):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', '_75nlfW')
        # records.append(results)

        for item in results:
            record = extract_record_flipkart(item)
            if record:  # Only append valid records
                records.append(record)

    # Close the driver
    driver.quit()

    return records
       


if __name__ == "__main__":
    search_term = input("Search term: ")
    main(search_term)
