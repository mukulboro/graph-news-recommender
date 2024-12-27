from db.database import LocalDatabase
from scraper.onlinekhabar_scraper import OnlinekhabarScraper
from scraper.ratopati_scraper import RatopatiScraper
from scraper.setopati_scraper import SetopatiScraper
import time
from clustering.cluster_news import ClusterNews
from news_threading.threading import ThreadScraping
from graphing.news_graph import NewsGraph

def scrape_and_process_news():
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
    end = time.time()
    
    return round(end-start, 2)

if __name__ == "__main__":
    itr = 1
    while True:
        time_taken = scrape_and_process_news()
        print(f"Completed Iteration [{itr}] in {time_taken} seconds\n\n")
        itr += 1
        # Scrape every 20 mins keeping in mind the time taken
        time.sleep(20*60 - time_taken)
        # ng = NewsGraph()
        # ng.get_shortest_path(source="c701d1c4d1e3e50dd2bef9c268837d71339937b341b2a01106d0120dace2430e",
        #                      destinaton="5126284ed8cb13d254ab49bb991e15c7ac4153ee520f5e92ef40f1a9958b7920")
        # break 
     

