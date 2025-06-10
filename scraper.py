import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://quotes.toscrape.com"
url = base_url  # Start with first page

all_quotes = []

while url:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')

    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        all_quotes.append([text, author, ", ".join(tags)])

    # Find the 'Next' button link if exists
    next_btn = soup.find('li', class_='next')
    if next_btn:
        next_page = next_btn.find('a')['href']
        url = base_url + next_page
    else:
        url = None  # No more pages

# Write all quotes to CSV
with open('quotes_all_pages.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Quote', 'Author', 'Tags'])
    writer.writerows(all_quotes)

print(f"Scraping complete! {len(all_quotes)} quotes saved to quotes_all_pages.csv")
