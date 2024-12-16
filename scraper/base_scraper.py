import requests
import bs4
import json

class NewsScraper:
    def __init__(self, json_dir="scraper/news_data.json"):
        self.json_dir = json_dir
    
    def __load_json_data(self):
        with open(self.json_dir, "r") as f:
            file_data = f.read()
            data = json.loads(file_data)
            return data
    
    def __scrape_websites(self, links):
        """
        Returns all scraped webpages listed in .json file
        if key is page_url and page2_url, this function returns
        {
            "page": <soup>
            "page2": <soup>
        }
        """
        page_data = dict()
        for i, key in enumerate(links):
            page_key = key.split("_")[0]
            response = requests.get(links[key])
            response.encoding = "utf-8"
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            page_data[f"{page_key}"] = soup
        return page_data

if __name__ == "__main__":
    test = NewsScraper()
    
