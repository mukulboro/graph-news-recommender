import sqlite3
import hashlib
from collections import defaultdict
import datetime as dt

"""
id = Hash of the news title
headline
body
url
image_url
website
category
published
processed = bool
in_graph = bool
"""

class LocalDatabase:
    def __init__(self, db_location="sqlite.db"):
        self.db_location = db_location
        # self.connection = sqlite3.connect(db_location)
        # self.cursor = self.connection.cursor()
        self.__create_table()

    def __create_table(self):
        query_news_table = """
                CREATE TABLE IF NOT EXISTS news(
                    id VARCHAR(256) PRIMARY KEY,
                    headline TEXT NOT NULL,
                    body TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    image_url TEXT NOT NULL,
                    website TEXT NOT NULL,
                    category TEXT NOT NULL,
                    published INTEGER NOT NULL,
                    processed INTEGER DEFAULT 0,
                    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
        
        query_cluster_table = """
            CREATE TABLE IF NOT EXISTS clusters(
                id VARCHAR(256),
                news_id VARCHAR(256),
                in_graph INTEGER DEFAULT 0,
                in_firebase INTEGER DEFAULT 0,
                PRIMARY KEY (id, news_id),
                FOREIGN KEY (news_id) REFERENCES news(id)
            )
        """
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query_news_table)
            cursor.execute(query_cluster_table)
        

    def insert_news(self, website:str, news_dict:dict):
        categories = news_dict.keys()
        new_news = 0
        for category in categories:
            news_list = news_dict[category]
            for news in news_list:
                headline:str = news["title"]
                id = hashlib.sha256(headline.encode('utf-8')).hexdigest()
                body = news["description"]
                url = news["url"]
                image_url = news["image"]
                published = int(news["published"])
                query = f"""
                INSERT INTO news (id, headline, body, url, image_url, website, category, published)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                try:
                    with sqlite3.connect(self.db_location) as connection:
                        cursor = connection.cursor()
                        cursor.execute(query,
                                    (id, headline, body, url, image_url, website, category, published))
                
                        connection.commit()
                    new_news += 1
                except sqlite3.IntegrityError as e:
                    continue
        print(f"{new_news} new news added from {website}")
        
    def get_unprocessed_news(self):
        all_data = list()
        today = dt.datetime.now()
        y, m, d = today.year, today.month, today.day
        today_utc = int(dt.datetime(y, m, d).timestamp())
        query = """
            SELECT * FROM NEWS WHERE processed = ? 
            OR published = ?
            ORDER BY published DESC
        """
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (0, today_utc))
            data = cursor.fetchall()
        for d in data:
            all_data.append({
                "key": d[0],
                "news": f"{d[1]} {d[2]}",
                "category": f"{d[-4]}"
            })
        return all_data
    
    def update_processed_news(self, news_list:list):
        # News list is a list of pk for all news
        query = """
        UPDATE news
        SET processed = 1
        WHERE id = ?
        """
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.executemany(query, [(news,) for news in news_list])
            connection.commit()
    
    def add_news_cluster(self, cluster:dict):
        cluster_id = cluster["keys"][0]
        for key in cluster["keys"]:
            query_check_if_exists = """
                SELECT * FROM clusters 
                WHERE news_id = ?
            """
            with sqlite3.connect(self.db_location) as connection:
                cursor = connection.cursor()
                cursor.execute(query_check_if_exists, (key,))
                check = cursor.fetchone()
                if check == None:
                    query = """
                            INSERT INTO clusters (id, news_id)
                            VALUES (?, ?)
                        """
                    cursor.execute(query, (cluster_id, key))
                else:
                    query = """
                        UPDATE clusters 
                        SET id = ?
                        WHERE news_id = ?
                    """
                    cursor.execute(query, (cluster_id, key)) 
                connection.commit()
            
    def get_clustered_news(self):
        # All news that have been clustered but not yet put in graph
        all_data = list()
        query = """
            SELECT * FROM
            clusters JOIN news 
            ON clusters.news_id = news.id
            WHERE clusters.in_graph = 0
            ORDER BY news.scraped_at DESC
        """
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        # Parse data in desired format
        for d in data:
            all_data.append({
                "cluster_id": d[0],
                "news_id": f"{d[1]}",
                "headline": f"{d[5]}",
                "body": f"{d[6]}",
                "url": f"{d[7]}",
                "image_url": f"{d[8]}",
                "website": f"{d[9]}",
                "category": f"{d[10]}",
                "published": f"{d[11]}",
                "scraped": f"{d[-1]}"
            })
        
        clusters = {}
        for item in all_data:
            cluster_id = item['cluster_id']
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    "cluster": cluster_id,
                    "category": item['category'], 
                    "published": item['published'],
                    "scraped": item["scraped"], 
                    "news": []
                }
            # Append the news article details
            clusters[cluster_id]['news'].append({
                "headline": item["headline"],
                "body": item["body"],
                "website": item["website"],
                "url": item["url"],
                "image_url": item["image_url"]
            })

        transformed_data = list(clusters.values())
        return transformed_data
    
    def update_cluster_in_graph(self, cluster_key:str):
        query = """
        UPDATE clusters
        SET in_graph = 1
        WHERE id = ?
        """
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (cluster_key,))
            connection.commit()
            
    def get_all_offline_news(self):
        all_data = list()
        query = """
            SELECT * FROM
            clusters JOIN news 
            ON clusters.news_id = news.id
            WHERE clusters.in_firebase = 0
            ORDER BY news.scraped_at DESC
        """
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        # Parse data in desired format
        for d in data:
            all_data.append({
                "cluster_id": d[0],
                "news_id": f"{d[1]}",
                "headline": f"{d[5]}",
                "body": f"{d[6]}",
                "url": f"{d[7]}",
                "image_url": f"{d[8]}",
                "website": f"{d[9]}",
                "category": f"{d[10]}",
                "published": f"{d[11]}",
                "scraped": f"{d[-1]}"
            })
        
        clusters = {}
        for item in all_data:
            cluster_id = item['cluster_id']
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    "cluster": cluster_id,
                    "category": item['category'], 
                    "published": item['published'],
                    "scraped": item["scraped"], 
                    "news": []
                }
            # Append the news article details
            clusters[cluster_id]['news'].append({
                "headline": item["headline"],
                "body": item["body"],
                "website": item["website"],
                "url": item["url"],
                "image_url": item["image_url"]
            })

        transformed_data = list(clusters.values())
        return transformed_data
    
    def update_news_in_firebase(self, key:str):
        query = """
        UPDATE clusters
        SET in_firebase = 1
        WHERE id = ?
        """
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (key,))
            connection.commit()
            
    def get_latest_news_by_category(self):
        query = """
            SELECT 
            n.category,
            c.id, 
            MAX(n.scraped_at) AS latest_published 
        FROM 
            news n JOIN clusters c ON n.id = c.news_id
        GROUP BY 
            n.category
        """
        data_dict = dict()
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            for d in data:
                data_dict[f"{d[0]}"] = d[1]
        return data_dict
    
    def get_latest_news(self):
        query = """
            SELECT 
            c.id
        FROM 
            news n JOIN clusters c ON n.id = c.news_id
        ORDER BY 
            n.scraped_at DESC
        LIMIT 100
        """
        news_list = []
        with sqlite3.connect(self.db_location) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            for d in data:
                news_list.append(d[0])
        return news_list