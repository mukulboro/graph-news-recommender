from scraper.setopati_scraper import SetopatiScraper
import pprint
if __name__ == "__main__":
    url = "https://www.bbc.com/news"
    scraper = SetopatiScraper()
    news = scraper.get_all_news()
    # pprint.pprint(news)