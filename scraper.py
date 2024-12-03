import requests
import bs4
import json
import time
class NewsScraper:
    def __init__(self):
        pass
    
    def __load_json_data(self):
        with open("news_data.json", "r") as f:
            file_data = f.read()
            data = json.loads(file_data)
            return data
    
    def __scrape_websites(self, links):
        page_data = dict()
        for i, key in enumerate(links):
            page_key = key.split("_")[0]
            response = requests.get(links[key])
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            page_data[f"{page_key}"] = soup
        return page_data
            
        
    def __parse_onlinekhabar(self, links):
        webpage_data = self.__scrape_websites(links)
        return webpage_data

    def get_all_news(self):
        news_data = self.__load_json_data()
        onlinekhabar = self.__parse_onlinekhabar(news_data["onlinekhabar"])
        return news_data
    
if __name__ == "__main__":
    url = "https://www.bbc.com/news"
    scraper = NewsScraper()
    start = time.time()
    news = scraper.get_all_news()
    end = time.time()
    print(f"Took: {end-start}s")