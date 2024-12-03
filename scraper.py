import requests
import bs4
import json

class NewsScraper:
    def __init__(self):
        pass
    
    def __load_json_data(self):
        with open("news_data.json", "r") as f:
            file_data = f.read()
            data = json.loads(file_data)
            return data
        
    def __scrape_onlinekhabar(self, links):
        print(links)
        pass

    def get_all_news(self):
        news_data = self.__load_json_data()
        onlinekhabar = self.__scrape_onlinekhabar(news_data["onlinekhabar"])
        # response = requests.get(self.url)
        # response.raise_for_status()
        # soup = bs4.BeautifulSoup(response.text, "html.parser")
        return news_data