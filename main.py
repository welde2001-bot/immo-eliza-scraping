from scraper.collect_urls import collect_urls
from scraper.scrape_properties import scrape_properties_from_file


def main():
    """Run full scraping pipeline."""
    print("Collecting property URLs...")
    collect_urls(output_file="data/urls.csv", max_pages=1)

    print("Scraping property details...")
    scrape_properties_from_file(input_file="data/urls.csv", output_file="data/properties.csv")

    print("Scraping finished.")


if __name__ == "__main__":
    main()
