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
            response.encoding = "utf-8"
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            page_data[f"{page_key}"] = soup
        return page_data
            
        
    def __parse_onlinekhabar(self, links):
        """
        Return data from onlinekhabar in format:
        {
            "breaking": [list]
            "national": [list]
            "intl": [list]
            "finance": [list]
            "entertainment": [list]
            "sports": [list]
        }

        Each news item has following 
        {
            "title": string
            "description": string
            "url": link
            "image": link
        }
        """
        webpages_data = self.__scrape_websites(links)

        # Work on getting breaking news first
        breaking_page:bs4.BeautifulSoup = webpages_data["homepage"]
        breaking_containers = breaking_page.find_all("section", {"class": "ok-bises"})
        breaking_news_list = []
        item:bs4.element.Tag
        for item in breaking_containers:
            news_item = dict()
            headline_parent = item.find("a")
            headline = headline_parent.get_text()
            headline_link = headline_parent.attrs["href"]
            # Extra request to get news description and image
            response = requests.get(headline_link)
            response.encoding = "utf-8"
            news_soup = bs4.BeautifulSoup(response.text, "html.parser")
            featured_image = (news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]
            top_paragraph = news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()
            news_item["description"] = top_paragraph
            news_item["title"] = headline
            news_item["url"] = headline_link
            news_item["image"] = featured_image
            breaking_news_list.append(news_item)
        return breaking_news_list

    def get_all_news(self):
        news_data = self.__load_json_data()
        onlinekhabar = self.__parse_onlinekhabar(news_data["onlinekhabar"])
        return onlinekhabar
    
if __name__ == "__main__":
    scraper = NewsScraper()
    news = scraper.get_all_news()
    print(news)