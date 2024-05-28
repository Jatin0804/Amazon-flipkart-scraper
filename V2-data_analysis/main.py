from components import Amazon_scraping
from components import flipkart
import csv
import json

# Ask for search term and run the scraper
search_term = input("Search term: ")


flipkart_records = flipkart.main(search_term)

# Write records to CSV
with open(f'files/flipkart/{search_term}.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Description', 'Price', 'Rating', 'Rating Count', 'URL'])
    writer.writerows(flipkart_records)


json_flipkart_records = [{key: value for key, value in zip(['Description', 'Price', 'Rating', 'Rating Count', 'URL'], record)} for record in flipkart_records]
with open(f'JSON_files/flipkart/{search_term}.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_flipkart_records, json_file, ensure_ascii=False, indent=4) 


amazon_records = Amazon_scraping.main(search_term)

# Write records to CSV
with open(f'files/amazon/{search_term}.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'URL'])
    writer.writerows(amazon_records)


json_amazon_records = [{key: value for key, value in zip(['Description', 'Price', 'Rating', 'Rating Count', 'URL'], record)} for record in amazon_records]
# Write records to JSON
with open(f'JSON_files/amazon/{search_term}.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_amazon_records, json_file, ensure_ascii=False, indent=4)