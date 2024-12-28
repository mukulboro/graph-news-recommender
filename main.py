from db.database import LocalDatabase
from scraper.onlinekhabar_scraper import OnlinekhabarScraper
from scraper.ratopati_scraper import RatopatiScraper
from scraper.setopati_scraper import SetopatiScraper
import time
from clustering.cluster_news import ClusterNews
from news_threading.threading import ThreadScraping
from graphing.news_graph import NewsGraph
from firebase.fb import FirebaseNews

def scrape_and_process_news(fb:FirebaseNews):
    start = time.time()
    # Initialize all objects needed
    ld = LocalDatabase()
    ts=ThreadScraping()
    os = OnlinekhabarScraper()
    print("Initialized ONLINEKHABAR")
    rs = RatopatiScraper()
    print("Initialized RATOPATI")
    ss = SetopatiScraper()
    print("Initialized SETOPATI")

    print("Initialized all objects")
    # Simultaneously Scrape all data from all websites
    news_data=ts.run(onlinekhabar=os,ratopati=rs,setopati=ss)
    # Insert data into database. Also cleans duplicate news
    ld.insert_news(website="onlinekhabar", news_dict=news_data['onlinekhabar'])
    ld.insert_news(website="ratopati", news_dict=news_data['ratopati'])
    ld.insert_news(website="setopati", news_dict=news_data['setopati'])
    # Init cluster object here as it depends on new news that has been added
    cluster = ClusterNews()
    # Insert all clustered news into database 
    cluster.parse_clusters()
    # Init graph object here as it depends on new clusters
    ng = NewsGraph()
    # Insert data in graph
    ng.build_graph()
    fb.upload_all_news()
    end = time.time()
    return round(end-start, 2)

if __name__ == "__main__":
    itr = 1
    # Initialize fb to prevent error
    firebase_app = FirebaseNews()
    while True:
        time_taken = scrape_and_process_news(fb=firebase_app)
        print(f"Completed Iteration [{itr}] in {time_taken} seconds\n\n")
        itr += 1
        # Scrape every 20 mins keeping in mind the time taken
        time.sleep(20*60 - time_taken)