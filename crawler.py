import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define the crawling interval (in seconds)
CRAWL_INTERVAL = 3600  # Set to 1 hour

# Target URL to crawl
target_url = "https://fortnite.gg/discover"  # Replace with your target URL

# Define a function to parse the HTML and extract the required data points
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_data = []
    islands = soup.find_all('a', class_='island')

    for island in islands:
        code = island['href'].split('=')[1] if 'href' in island.attrs else None
        title_tag = island.find('h3', class_='island-title')
        title = title_tag.get_text(strip=True) if title_tag else None
        players_tag = island.find('div', class_='players')
        players = players_tag.get_text(strip=True) if players_tag else None

        extracted_data.append({
            'Island Title': title,
            'Island Code': code,
            'Players': players,
        })

    return pd.DataFrame(extracted_data)

# Define the main crawling and parsing logic
def crawl_and_parse():
    """
    Main function to crawl the target URL, parse the HTML, and extract data.
    """
    try:
        print("Starting crawl...")
        response = requests.get(target_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        html_content = response.text
        print("Crawl complete. Parsing HTML...")

        # Parse the HTML content
        parsed_data = parse_html(html_content)

        # Output results to a CSV
        output_file = 'extracted_data.csv'
        parsed_data.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

    except Exception as e:
        print(f"Error during crawl or parsing: {e}")

# Main script loop
if __name__ == "__main__":
    while True:
        crawl_and_parse()
        print(f"Sleeping for {CRAWL_INTERVAL} seconds...")
        time.sleep(CRAWL_INTERVAL)
