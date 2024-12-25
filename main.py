from db.database import LocalDatabase
from scraper.onlinekhabar_scraper import OnlinekhabarScraper
from scraper.ratopati_scraper import RatopatiScraper
from scraper.setopati_scraper import SetopatiScraper
import time
from clustering.cluster_news import ClusterNews
from news_threading.threading import ThreadScraping
import json

if __name__ == "__main__":
    
    while True:
        os = OnlinekhabarScraper()
        rs = RatopatiScraper()
        ss = SetopatiScraper()
        ts=ThreadScraping()
        ld = LocalDatabase()
        
        start = time.time()
        news_data=ts.run(onlinekhabar=os,ratopati=rs,setopati=ss)
        end=time.time()

        print(f"Completed all scraping in {end-start} seconds\n\n")

        ld.insert_news(website="onlinekhabar", news_dict=news_data['onlinekhabar'])
        ld.insert_news(website="ratopati", news_dict=news_data['ratopati'])
        ld.insert_news(website="setopati", news_dict=news_data['setopati'])
       
        cluster = ClusterNews()
        all_clusters = cluster.parse_clusters()
        # clustered = ld.get_clustered_news()
        # print(len(clustered))
        
        # with open("clusters.json", "w") as f:
        #     f.write(json.dumps(clustered, ensure_ascii=False))
            
        # Sleep for 20 mins till next scraping
        time.sleep(20*60)
    
