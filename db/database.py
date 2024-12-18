import sqlite3
import hashlib
import pprint

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
        self.connection = sqlite3.connect(db_location)
        self.cursor = self.connection.cursor()
        self.__create_table()

    def __create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS news(
                    id VARCHAR(256) PRIMARY KEY,
                    headline TEXT NOT NULL,
                    body TEXT NOT NULL,
                    url TEXT NOT NULL,
                    image_url TEXT NOT NULL,
                    website TEXT NOT NULL,
                    category TEXT NOT NULL,
                    published INTEGER NOT NULL,
                    processed INTEGER DEFAULT 0,
                    in_graph INTEGER DEFAULT 0
                )
                """
        self.cursor.execute(query)

    def insert_news(self, website:str, news_dict:dict):
        categories = news_dict.keys()
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
                    self.cursor.execute(query,
                                    (id, headline, body, url, image_url, website, category, published))
                
                    self.connection.commit()
                except sqlite3.IntegrityError as e:
                    continue
