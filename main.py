from scraper.onlinekhabar_scraper import OnlinekhabarScraper
from scraper.ratopati_scraper import RatopatiScraper
import pprint
if __name__ == "__main__":
    # scraper = OnlinekhabarScraper()
    # news = scraper.get_all_news()
    # pprint.pprint(news)

    ratoscraper=RatopatiScraper()
    rato_news=ratoscraper.get_all_news()
    pprint.pprint(rato_news)