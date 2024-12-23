from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from db.database import LocalDatabase
from collections import defaultdict
from nepali_stemmer.stemmer import NepStemmer


class ClusterNews:
    def __init__(self, stopwords_dir="clustering/stopwords.txt"):
        self.news = list()
        self.database = LocalDatabase()
        self.stopwords_dir = stopwords_dir
        self.all_news = self.database.get_unprocessed_news()
        for news in self.all_news:
            stemmed_news = self.__stem_news(news=news["news"])
            self.news.append(stemmed_news)
    
    def __stem_news(self, news):
        nepstem = NepStemmer()
        with open(self.stopwords_dir, 'r') as f:
            stopwords = f.readlines()
        stemmed_news = nepstem.stem(news)
        news_words = stemmed_news.split(" ")
        filtered_sentence = [word for word in news_words if word.strip() not in stopwords]
        result = " ".join(filtered_sentence)
        return result

    def __vectorize_news(self):
        if len(self.news) > 0:
            tfidf = TfidfVectorizer()
            tfidf_matrix = tfidf.fit_transform(self.news)
            return tfidf_matrix

    def __get_difference_matrix(self):
        tfidf_matrix = self.__vectorize_news()
        cosine_sim = cosine_similarity(tfidf_matrix)
        distance_matrix = 1 - cosine_sim  # Convert similarity to distance
        return distance_matrix
    
    def __cluster_news(self):
        if len(self.news) > 1: # AG Clustering requires at least 2 items
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
        else:
            return []
        
    def __plot_custers(self):
        try:
            distance_matrix = self.__get_difference_matrix()
            linked = linkage(distance_matrix, 'average')
            # Plot dendrogram
            plt.figure(figsize=(8, 6))
            dendrogram(
                linked,
                orientation='top',
                color_threshold= 0.5,
                # labels=dendrogram_labels,
                distance_sort='descending',
                show_leaf_counts=True
            )
            plt.title("Hierarchical Clustering Dendrogram")
            plt.xlabel("News Headlines/Paragraphs")
            plt.ylabel("Distance")
            plt.savefig("Test.png")
        except BaseException as e:
            print("Euta ni news na vayera plot garina hehehe")
        
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
            








