import networkx as nx
import pickle
import time
import math
from db.database import LocalDatabase
import os
import datetime as dt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ClusterNode:
    # Special class to store all data about the cluster in node
    def __init__(self, cluster:dict):
        self.key = cluster["cluster"]
        self.category = cluster["category"]
        self.published = int(cluster["published"])
        self.headline = cluster["news"][0]["headline"]
        self.body = cluster["news"][0]["body"]
        self.scraped = self.__parse_scraped(cluster["scraped"])
        
    def __parse_scraped(self, date_str:str)->int:
        date = date_str.split(" ")
        y, mo, d = date[0].split("-")
        h, mi, s = date[1].split(":")
        parsed_date = dt.datetime(year=int(y), month=int(mo), day=int(d),
                                  hour=int(h), minute=int(mi), second=int(s))
        return int(parsed_date.timestamp())
    
    def __repr__(self):
        return self.key

class NewsGraph:
    def __init__(self, 
                 scrape_frequency = 20*60, 
                 edge_threshold = 0.3,
                 backup_location="backups/graphs/"):
        self.scrape_fq = scrape_frequency # in seconds
        self.edge_thrs = edge_threshold
        self.backup_dir = backup_location
    
        self.__load_graph()
        self.current_backup = int(time.time()) # File to use to hold backup of current instance
        
        self.db = LocalDatabase()
        self.all_clusters = self.db.get_clustered_news()
        
    def __load_graph(self):
        backup_list = os.listdir(self.backup_dir)
        if backup_list == []:
            self.graph = nx.Graph()
        else:
            backup_list = sorted(backup_list, key= lambda x: int(x.split(".")[0]))
            latest_graph = backup_list[-1]
            with open(os.path.join(self.backup_dir, latest_graph), 'rb') as p:
                self.graph = pickle.load(p)
        
    def __save_graph(self):
        with open(os.path.join(self.backup_dir, f"{self.current_backup}.pkl"), "wb") as p:
            pickle.dump(self.graph, p)
    
    def __get_published_day_score(self, day1, day2):
        # Both days are in UTC seconds
        delta = abs(day1-day2)
        # ⌊ |cos(Δday)| ⌋
        return math.floor( abs( math.cos(delta) ) )
    
    def __get_cosine_similarity_score(self, news1, news2):
        news_list = [news1, news2]
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(news_list)
        cosine_sim = cosine_similarity(tfidf_matrix)
        return cosine_sim[0, 1]

    def __get_category_score(self, category1, category2):
        if category1 == category1:
            return 1
        return 0
    
    def __get_scrape_time_score(self, scrape1, scrape2):
        # e^(-x/12)
        # x = (|scrape1 - scrape2|)/ scrape freq
        x = abs(scrape1 - scrape2)/self.scrape_fq
        return math.exp(-x/12)
    
    def __get_edge_weight(self, news1:ClusterNode, news2:ClusterNode):
        publication_day_score = self.__get_published_day_score(day1=news1.published,
                                                               day2=news2.published) 
        cosine_sim_score = self.__get_cosine_similarity_score(news1=f"{news1.headline} {news1.body}",
                                                              news2=f"{news2.headline} {news2.body}")
        category_score = self.__get_category_score(category1=news1.category,
                                                   category2=news2.category)
        scraping_time_score = self.__get_scrape_time_score(scrape1=news1.scraped,
                                                           scrape2=news2.scraped)
        # Edge Score = (2PubScore + 3CosSim + 2CatScore + ScrapeScore)/7
        
        edge_score = (2*publication_day_score + 3*cosine_sim_score +
                      2*category_score + scraping_time_score) / 7
        if edge_score > self.edge_thrs:
            # Return complement of edge score
            # so shortest path algorith finds the
            # news with the most similarity
            return round(1-edge_score, 4)
        else:
            return None
    
    def __get_node_color(self, category:str)->str:
        match category:
            case "breaking":
                return "red"
            case "national":
                return "green"
            case "intl":
                return "blue"
            case "finance":
                return "yellow"
            case "entertainment":
                return "purple"
            case "sports":
                return "orange"
            case _:
                return "white"

    def build_graph(self):
        self.__load_graph()
        clusters = self.all_clusters
        for cluster in clusters:
            cluster_node = ClusterNode(cluster=cluster)
            node_list = list(self.graph.nodes)
            edge_list = []
            for graph_node in node_list:
                edge_weight = self.__get_edge_weight(cluster_node, graph_node)
                if not edge_weight == None:
                    edge_list.append( (cluster_node, graph_node, edge_weight) )
            self.graph.add_node(cluster_node, color=self.__get_node_color(cluster_node.category))
            self.graph.add_weighted_edges_from(edge_list)
            print(f"Added Node {cluster_node} with {len(edge_list)} edges")
            self.__save_graph()
            self.db.update_cluster_in_graph(cluster_key=cluster_node.key)
    
