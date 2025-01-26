from graphing.news_graph import NewsGraph, ClusterNode
from db.database import LocalDatabase

class Recommender:
    def __init__(self, user_pref:dict, number_of_news = 100):
        """
        user_pref expects the following
        {
            "category1": {
                "news_list": list of keys
            },
            "category2": {
                "news_list": list of keys
            }
        }
        """
        self.graph = NewsGraph()
        self.db = LocalDatabase()
        self.latest_news_category = self.db.get_latest_news_by_category()
        self.prefs = user_pref
        self.news_no = number_of_news
    
    def __get_recommended_list(self):
        all_news = []
        for i,key in enumerate(self.latest_news_category):
            latest_news = self.latest_news_category[key]
            for pref_news in self.prefs[key]["news_list"]:
                news_path = self.graph.get_shortest_path(source=pref_news,
                                                         destinaton=latest_news)
                news_path = [x for x in news_path if not x.key == pref_news]
                all_news.extend(news_path)
        all_news = sorted(all_news,key= lambda x : -x.scraped)
        all_news_processed = [x.key for x in all_news]
        return list(set(all_news_processed))
    
    def get_all_news(self):
        recommended_news = self.__get_recommended_list()
        all_latest_news = self.db.get_latest_news()
        news_needed = self.news_no - len(recommended_news)
        if news_needed <= 0:
            return recommended_news
        all_news = []
        all_news.extend(recommended_news)
        for news in all_latest_news:
            if news not in all_news:
                all_news.append(news)
            if len(set(all_news)) == self.news_no:
                break
        
        return all_news
            