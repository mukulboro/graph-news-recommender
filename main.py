from db.database import LocalDatabase
from scraper.onlinekhabar_scraper import OnlinekhabarScraper
from scraper.ratopati_scraper import RatopatiScraper
from scraper.setopati_scraper import SetopatiScraper
import time
from clustering.cluster_news import ClusterNews
import json

if __name__ == "__main__":
    ld = LocalDatabase()
    start = time.time()
    os = OnlinekhabarScraper()
    os_data = os.get_all_news()

    rs = RatopatiScraper()
    rs_data = rs.get_all_news()

    ss = SetopatiScraper()
    ss_data = ss.get_all_news()
    end = time.time()

    print(f"Completed all scraping in {end-start} seconds")

    ld.insert_news(website="onlinekhabar", news_dict=os_data)
    ld.insert_news(website="ratopati", news_dict=rs_data)
    ld.insert_news(website="setopati", news_dict=ss_data)

    cluster = ClusterNews()
    all_clusters = cluster.parse_clusters()
    clustered = ld.get_clustered_news()
    
    with open("clusters.json", "w") as f:
        f.write(json.dumps(clustered, ensure_ascii=False))
    
