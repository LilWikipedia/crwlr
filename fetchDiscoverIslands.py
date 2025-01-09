from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json

async def extract_fortnite_ugc_content():
    # Initialize browser config
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True
    )
    
    # Initialize crawler config with JSON CSS extraction strategy
    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Fortnite UGC Discover",
                "baseSelector": "a.island",  # Selector for each UGC content block
                "fields": [
                    {
                        "name": "island_code",
                        "selector": "",
                        "type": "text",
                        "attribute": "href",
                        "transform": "lambda href: href.split('=')[1] if href else None"
                    },
                    {
                        "name": "title",
                        "selector": "h3.island-title",
                        "type": "text"
                    },
                    {
                        "name": "players",
                        "selector": "div.players",
                        "type": "text"
                    }
                ]
            }
        )
    )

    # URL of the Fortnite Discover page (replace with your actual URL)
    url = "https://www.fortnite.gg/discover/"

    # Use context manager for proper resource handling
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Extract the data
        result = await crawler.arun(url=url, config=crawler_config)
        
        # Process and print the results
        if result and result.extracted_content:
            # Parse the JSON string into a list of UGC items
            ugc_items = json.loads(result.extracted_content)
            
            # Save the data to a JSON file or CSV as needed
            output_file = "fortnite_ugc_content.json"
            with open(output_file, "w") as file:
                json.dump(ugc_items, file, indent=4)
            
            print(f"Extracted data saved to {output_file}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(extract_fortnite_ugc_content())
