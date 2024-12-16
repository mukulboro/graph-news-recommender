from scraper.onlinekhabar_scraper import OnlinekhabarScraper

if __name__ == "__main__":
    url = "https://www.bbc.com/news"
    scraper = OnlinekhabarScraper()
    news = scraper.get_all_news()
    