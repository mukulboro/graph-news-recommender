from .base_scraper import NewsScraper
import bs4
import requests
from .base_scraper import logger

class SetopatiScraper(NewsScraper):
    def __init__(self):
        super().__init__()
        logger.info("Initialized SETOPATI scraper")
        self.news_data = self._NewsScraper__load_json_data()
        self.webpages_data = self._NewsScraper__scrape_websites(self.news_data["setopati"])
    
    def __parse_publication_date(self, date_str:str):
        temp = date_str.split(":")[1].split(",")
        year = temp[-1][0:5].strip()
        date = temp[1].strip().split(" ")[-1].strip()
        month = temp[1].strip().split(" ")[0].strip()
        unix_timestamp = self._NewsScraper__parse_nepali_date("setopati",year, month, date)
        return unix_timestamp
    
    def __get_breaking_news(self):
        try:
            breaking_page:bs4.BeautifulSoup = self.webpages_data["homepage"]
            breaking_container = breaking_page.find_all("div", {"class":"breaking-news-item"})
            breaking_container = [x.find("a") for x in breaking_container]
            breaking_news_list = []
            item:bs4.element.Tag
            for item in breaking_container:
                news_item = dict()
                headline_link = item.attrs["href"]
                headline = item.attrs["title"].strip()
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = news_soup.find("figure", {"class":"new-featured-image"}).find("img").attrs["src"].strip()
                top_paragraph = news_soup.find("div", {"class":"editor-box"}).find("p").get_text().strip()
                published_date = news_soup.find("span", {"class":"pub-date"}).get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph.replace("\xa0", " ").replace("\u200d", "")
                news_item["title"] = headline.replace("\xa0", " ").replace("\u200d", "")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                breaking_news_list.append(news_item)
        except BaseException as e:
            raise(e)
        return breaking_news_list
    
    def __get_business_news(self):
        try:
            page:bs4.BeautifulSoup = self.webpages_data["finance"]
            container = page.find_all("div", {"class":"items"})[:10]
            container = [x.find("a") for x in container]
            news_list = []
            item:bs4.element.Tag
            for item in container:
                news_item = dict()
                headline_link = item.attrs["href"]
                headline = item.attrs["title"].strip()
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = news_soup.find("figure", {"class":"new-featured-image"}).find("img").attrs["src"].strip()
                top_paragraph = news_soup.find("div", {"class":"editor-box"}).find("p").get_text().strip()
                published_date = news_soup.find("span", {"class":"pub-date"}).get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph.replace("\xa0", " ").replace("\u200d", "")
                news_item["title"] = headline.replace("\xa0", " ").replace("\u200d", "")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                news_list.append(news_item)
        except BaseException as e:
            raise(e)
        return news_list
    
    def __get_entertainment_news(self):
        try:
            page:bs4.BeautifulSoup = self.webpages_data["entertainment"]
            container = page.find_all("div", {"class":"items"})[:10]
            container = [x.find("a") for x in container]
            news_list = []
            item:bs4.element.Tag
            for item in container:
                news_item = dict()
                headline_link = item.attrs["href"]
                headline = item.attrs["title"].strip()
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = news_soup.find("figure", {"class":"new-featured-image"}).find("img").attrs["src"].strip()
                top_paragraph = news_soup.find("div", {"class":"editor-box"}).find("p").get_text().strip()
                published_date = news_soup.find("span", {"class":"pub-date"}).get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph.replace("\xa0", " ").replace("\u200d", "")
                news_item["title"] = headline.replace("\xa0", " ").replace("\u200d", "")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                news_list.append(news_item)
        except BaseException as e:
            raise(e)
        return news_list
    
    def __get_intl_news(self):
        try:
            page:bs4.BeautifulSoup = self.webpages_data["intl"]
            container = page.find_all("div", {"class":"items"})[:10]
            container = [x.find("a") for x in container]
            news_list = []
            item:bs4.element.Tag
            for item in container:
                news_item = dict()
                headline_link = item.attrs["href"]
                headline = item.attrs["title"].strip()
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = news_soup.find("figure", {"class":"new-featured-image"}).find("img").attrs["src"].strip()
                top_paragraph = news_soup.find("div", {"class":"editor-box"}).find("p").get_text().strip()
                published_date = news_soup.find("span", {"class":"pub-date"}).get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph.replace("\xa0", " ").replace("\u200d", "")
                news_item["title"] = headline.replace("\xa0", " ").replace("\u200d", "")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                news_list.append(news_item)
        except BaseException as e:
            raise(e)
        return news_list
    
    def __get_national_news(self):
        try:
            page:bs4.BeautifulSoup = self.webpages_data["national"]
            container = page.find_all("div", {"class":"items"})[:10]
            container = [x.find("a") for x in container]
            news_list = []
            item:bs4.element.Tag
            for item in container:
                news_item = dict()
                headline_link = item.attrs["href"]
                headline = item.attrs["title"].strip()
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = news_soup.find("figure", {"class":"new-featured-image"}).find("img").attrs["src"].strip()
                top_paragraph = news_soup.find("div", {"class":"editor-box"}).find("p").get_text().strip()
                published_date = news_soup.find("span", {"class":"pub-date"}).get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph.replace("\xa0", " ").replace("\u200d", "")
                news_item["title"] = headline.replace("\xa0", " ").replace("\u200d", "")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                news_list.append(news_item)
        except BaseException as e:
            raise(e)
        return news_list
    
    def __get_sports_news(self):
        try:
            page:bs4.BeautifulSoup = self.webpages_data["sports"]
            container = page.find_all("div", {"class":"items"})[:10]
            container = [x.find("a") for x in container]
            news_list = []
            item:bs4.element.Tag
            for item in container:
                news_item = dict()
                headline_link = item.attrs["href"]
                headline = item.attrs["title"].strip()
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = news_soup.find("figure", {"class":"new-featured-image"}).find("img").attrs["src"].strip()
                top_paragraph = news_soup.find("div", {"class":"editor-box"}).find("p").get_text().strip()
                published_date = news_soup.find("span", {"class":"pub-date"}).get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph.replace("\xa0", " ").replace("\u200d", "")
                news_item["title"] = headline.replace("\xa0", " ").replace("\u200d", "")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                news_list.append(news_item)
        except BaseException as e:
            raise(e)
        return news_list

    def get_all_news(self):
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
            "published": int [unix time of publication]
        }
        """
        return {
            "breaking": self.__get_breaking_news(),
            "national": self.__get_national_news(),
            "intl": self.__get_intl_news(),
            "finance": self.__get_business_news(),
            "entertainment": self.__get_entertainment_news(),
            "sports": self.__get_sports_news()
        }