from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from db.database import LocalDatabase
from collections import defaultdict

class ClusterNews:
    def __init__(self):
        self.news = list()
        self.database = LocalDatabase()
        self.all_news = self.database.get_unprocessed_news()
        for news in self.all_news:
            self.news.append(news["news"])

    def __vectorize_news(self):
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(self.news)
        return tfidf_matrix

    def __get_difference_matrix(self):
        tfidf_matrix = self.__vectorize_news()
        cosine_sim = cosine_similarity(tfidf_matrix)
        distance_matrix = 1 - cosine_sim  # Convert similarity to distance
        return distance_matrix
    
    def __cluster_news(self):
        if len(self.news) > 0:
            distance_matrix = self.__get_difference_matrix()
            clustering = AgglomerativeClustering(
            metric='precomputed',  
            linkage='average',  
            n_clusters=None,  
            distance_threshold=0.3  # Decided based on experimentation
            )
            clustering.fit(distance_matrix)
            news_clusters = clustering.labels_
            return news_clusters
        
    def __plot_custers(self):
        distance_matrix = self.__get_difference_matrix()
        linked = linkage(distance_matrix, 'average')
        # Plot dendrogram
        plt.figure(figsize=(8, 6))
        dendrogram(
            linked,
            orientation='top',
            # labels=dendrogram_labels,
            distance_sort='descending',
            show_leaf_counts=True
        )
        plt.title("Hierarchical Clustering Dendrogram")
        plt.xlabel("News Headlines/Paragraphs")
        plt.ylabel("Distance")
        plt.savefig("Test.png")
        
    def __assign_clusters(self):
        all_clusters = list()
        news_clusters = self.__cluster_news()
        # self.__plot_custers()
        if len(self.news) > 0:
            for i, cluster in enumerate(news_clusters):
                all_clusters.append({
                    "cluster": int(cluster),
                    "key": self.all_news[i]["key"],
                    "news": self.all_news[i]["news"]
                })
        return all_clusters
    
    def parse_clusters(self):
        all_clusters = self.__assign_clusters()
        clustered_data = defaultdict(lambda: {"news": [], "keys": []})
        for item in all_clusters:
            clustered_data[item["cluster"]]["news"].append(item["news"])
            clustered_data[item["cluster"]]["keys"].append(item["key"])

        # Convert to desired format
        result = [{"cluster": cluster, **values} for cluster, values in clustered_data.items()]
        result = sorted(result, key=lambda x: x["cluster"])
        
        # Add all clustered news into database
        for r in result:
            self.database.add_news_cluster(r)
            # Update the processed value of all clustered news
            self.database.update_processed_news(news_list=r["keys"])
        
        self.__plot_custers()
        return result
            








