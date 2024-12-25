import networkx as nx
import pickle
import math
from db.database import LocalDatabase

class NewsGraph:
    def __init__(self, scrape_frequency = 20*60, edge_threshold = 0.27):
        self.scrape_fq = scrape_frequency # in seconds
        self.edge_thrs = edge_threshold
        self.db = LocalDatabase()
        self.all_clusters = self.db.get_clustered_news()
    
    def __load_graph(self):
        # If graph backups exist, load latest backup
        # Else create new graph
        pass
    
    def __get_published_day_score(self, day1, day2):
        # Both days are in UTC seconds
        delta = abs(day1-day2)
        # ⌊ |cos(Δday)| ⌋
        return math.floor( abs( math.cos(delta) ) )
    
    def __get_cosine_similarity_score(self, news1, news2):
        # Calculate and return similarity score
        pass
    
    def __get_category_score(self, category1, category2):
        if category1 == category1:
            return 1
        return 0
    
    def __get_scrape_time_score(self, scrape1, scrape2):
        # e^(-x/12)
        # x = (|scrape1 - scrape2|)/ scrape freq
        x = abs(scrape1 - scrape2)/self.scrape_fq
        return math.exp(-x/12)
    
    def __get_edge_weight(self, news_key_1, news_key_2):
        # Nodes only hold the cluster key
        # First get all relevant data from db
        news1_dict = self.db.get_single_cluster(cluster_key=news_key_1)
        news2_dict = self.db.get_single_cluster(cluster_key=news_key_2)
        
        publication_day_score = self.__get_published_day_score(day1=news1_dict["published"],
                                                               day2=news2_dict["published"]) 
        cosine_sim_score = self.__get_cosine_similarity_score(news1=news1_dict["news"],
                                                              news2=news2_dict["news"])
        category_score = self.__get_category_score(category1=news1_dict["category"],
                                                   category2=news2_dict["category"])
        scraping_time_score = self.__get_scrape_time_score(scrape1=news1_dict["scrape_time"],
                                                           scrape2=news2_dict["scrape_time"])
        # Edge Score = (2PubScore + 3CosSim + 2CatScore + ScrapeScore)/7
        
        edge_score = (2*publication_day_score + 3*cosine_sim_score +
                      2*category_score + scraping_time_score) / 7
        if edge_score > self.edge_thrs:
            # Return complement of edge score
            # so shortest path algorith finds the
            # news with the most similarity
            return 1 - edge_score
        else:
            return None

G = nx.Graph()
print(G)
