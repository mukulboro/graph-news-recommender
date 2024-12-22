from db.database import LocalDatabase
from scraper.onlinekhabar_scraper import OnlinekhabarScraper
from scraper.ratopati_scraper import RatopatiScraper
from scraper.setopati_scraper import SetopatiScraper
import time
from Threading.threading import ThreadScraping

if __name__ == "__main__":
    ld = LocalDatabase()
    start=time.time()
    os = OnlinekhabarScraper()
    # os.get_all_news()
    rs = RatopatiScraper()
    # rs.get_all_news()
    ss = SetopatiScraper()
    # ss.get_all_news()
    tr=ThreadScraping()
    news_data=tr.run(onlinekhabar=os,ratopati=rs,setopati=ss)
    end=time.time()
    print(f"Completed all scraping in {end-start} seconds")
        
    ld.insert_news(website="onlinekhabar", news_dict=news_data['onlinekhabar'])
    ld.insert_news(website="ratopati", news_dict=news_data['ratopati'])
    ld.insert_news(website="setopati", news_dict=news_data['setopati'])


