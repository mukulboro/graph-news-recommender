from scraper import NewsScraper

if __name__ == "__main__":
    url = "https://www.bbc.com/news"
    scraper = NewsScraper()
    news = scraper.get_all_news()
    # print(news)