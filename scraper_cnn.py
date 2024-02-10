import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 

# Constants
BASE_URL = 'https://edition.cnn.com/article/sitemap-2023-'
PAGE_RANGE = range(1, 13)

def build_url(base_url, page_number):
    """Builds and returns the individual URLs to scrape."""
    return f'{base_url}{page_number}.html'

def make_request(url):
    """Makes a GET request to the given URL and returns a BeautifulSoup object."""
    try:
        with requests.get(url) as response:
            return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Failed to make request to {url}. Error: {e}")
        return None

def get_entries(soup):
    """Returns all 'div' elements (poor composed HTML) from the given BeautifulSoup object."""
    return soup.find_all('div', class_='sitemap-entry') if soup else []

def extract_data(entry):
    """Extracts and returns the date, content, and link from the given entry."""
    news_entries = entry.find_all('li')
    entries_with_date = []
    for news_entry in news_entries:
        date_span = news_entry.find('span', class_='date')
        content_span = news_entry.find('span', class_='sitemap-link')
        link = news_entry.find('a')
        if date_span and content_span and link:
            entries_with_date.append({
                'date': date_span.text.strip(),
                'content': content_span.text.strip(),
                'link' : link.get('href')
            })
    return entries_with_date

def scrape_cnn(base_url, page_range, max_sleep_time=5):
    """Scrapes CNN sitemap and returns a list of entries with date, content, and link."""
    all_entries = []
    for page_number in page_range:
        url = build_url(base_url, page_number)
        soup = make_request(url)
        sitemap_entries = get_entries(soup)
        for entry in sitemap_entries:
            all_entries.extend(extract_data(entry))
        time.sleep(random.randint(1, max_sleep_time))  # Sleep to avoid overloading the server
    return all_entries

def main():
    """Main function to run the scraper and save the results to a CSV file."""
    entries = scrape_cnn(BASE_URL, PAGE_RANGE)
    df = pd.DataFrame(entries)
    df.to_csv('CNN_2023.csv', index=False)

if __name__ == '__main__':
    main()



