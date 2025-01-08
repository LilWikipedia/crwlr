import time
from crawler import crawl_and_parse

# Define how often to crawl the site (in seconds)
CRAWL_INTERVAL = 3600  # 1 hour

if __name__ == "__main__":
    while True:
        print("Starting the crawling process...")
        crawl_and_parse()
        print(f"Sleeping for {CRAWL_INTERVAL} seconds...")
        time.sleep(CRAWL_INTERVAL)
