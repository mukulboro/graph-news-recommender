from .base_scraper import NewsScraper
import bs4
import requests

class OnlinekhabarScraper(NewsScraper):
    def __init__(self):
        super().__init__()
        self.news_data = self._NewsScraper__load_json_data()
        self.webpages_data = self._NewsScraper__scrape_websites(self.news_data["onlinekhabar"])
    
    def __parse_publication_date(self, date_str:str):
        year, month, _, date, __, ___= date_str.split(" ")
        unix_timestamp = self._NewsScraper__parse_nepali_date("onlinekhabar",year, month, date)
        return unix_timestamp

    def __get_breaking_news(self):
        breaking_page:bs4.BeautifulSoup = self.webpages_data["homepage"]
        breaking_containers = breaking_page.find_all("section", {"class": "ok-bises"})
        breaking_news_list = []
        item:bs4.element.Tag
        for item in breaking_containers:
            try:
                news_item = dict()
                headline_parent = item.find("a")
                headline = (headline_parent.get_text()).strip()
                headline_link = (headline_parent.attrs["href"]).strip()
                # Extra request to get news description and image
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = ((news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]).strip()
                top_paragraph = (news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()).strip()
                published_date = news_soup.find("div", {"class":"ok-news-post-hour"}).find("span").get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                breaking_news_list.append(news_item)
            except BaseException as e:
                print(e)
        return breaking_news_list
    
    def __get_business_news(self):
        business_page:bs4.BeautifulSoup = self.webpages_data["finance"]
        # Have to scrape multiple containers to get info
        business_containers = business_page.find("div", {"id":"featured-carousel"}).find_all("div", {"class":"ok-news-post"})
        business_containers = [x.find("a") for x in business_containers]
        business_heros = business_page.find_all("div", {"class":"post-title-wrap"})
        business_heros = [x.find("h4").find("a") for x in business_heros]
        all_business_links = business_containers + business_heros
        business_news_list = []
        item:bs4.element.Tag
        for item in all_business_links:
            try:
                news_item = dict()
                headline = item.get_text().strip()
                headline_link = item.attrs["href"]
                # Extra request to get news description and image
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = ((news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]).strip()
                top_paragraph = (news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()).strip()
                published_date = news_soup.find("div", {"class":"ok-news-post-hour"}).find("span").get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                business_news_list.append(news_item)
            except BaseException as e:
                continue
        return business_news_list
    
    def __get_entertainment_news(self):
        entertainment_page:bs4.BeautifulSoup = self.webpages_data["entertainment"]
        entertainment_containers = entertainment_page.find("div", {"class":"ok-col-left"}).find_all("div", {"class":"ok-news-post"})[:10]
        entertainment_containers = [x.find("a") for x in entertainment_containers]
        item:bs4.element.Tag
        entertainment_links = []
        for item in entertainment_containers:
            try:
                news_item = dict()
                headline_link = item.attrs["href"]
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = ((news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]).strip()
                top_paragraph = (news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()).strip()
                headline = news_soup.find("h1").get_text().strip()
                published_date = news_soup.find("div", {"class":"ok-news-post-hour"}).find("span").get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                entertainment_links.append(news_item)
            except BaseException as e:
                continue
        return entertainment_links
    
    def __get_intl_news(self):
        intl_page:bs4.BeautifulSoup = self.webpages_data["intl"]
        intl_containers = intl_page.find("div", {"class":"ok-col-left"}).find_all("div", {"class":"ok-news-post"})[:10]
        intl_containers = [x.find("a") for x in intl_containers]
        item:bs4.element.Tag
        intl_links = []
        for item in intl_containers:
            try:
                news_item = dict()
                headline_link = item.attrs["href"]
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                featured_image = ((news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]).strip()
                top_paragraph = (news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()).strip()
                headline = news_soup.find("h1").get_text().strip()
                published_date = news_soup.find("div", {"class":"ok-news-post-hour"}).find("span").get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                intl_links.append(news_item)
            except BaseException as e:
                continue
        return intl_links
    
    def __get_national_news(self):
        national_page:bs4.BeautifulSoup = self.webpages_data["national"]
        national_containers = national_page.find("div", {"class":"ok-col-left"}).find_all("div", {"class":"ok-news-post"})[:10]
        national_containers = [x.find("a") for x in national_containers]
        item:bs4.element.Tag
        national_links = []
        for item in national_containers:
            try:
                news_item = dict()
                headline_link = item.attrs["href"]
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                headline = news_soup.find("h1").get_text().strip()
                featured_image = ((news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]).strip()
                top_paragraph = (news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()).strip()
                published_date = news_soup.find("div", {"class":"ok-news-post-hour"}).find("span").get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                national_links.append(news_item)
            except BaseException as e:
                continue
        return national_links
    
    def __get_sports_news(self):
        sports_page:bs4.BeautifulSoup = self.webpages_data["sports"]
        sport_containers = sports_page.find_all("div", {"class":"okv4-post-content"})[:10]
        sport_containers = [x.find("h2").find("a") for x in sport_containers]
        item:bs4.element.Tag
        sport_links = []
        for item in sport_containers:
            try:
                news_item = dict()
                headline_link = item.attrs["href"]
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")
                headline = news_soup.find("h1").get_text().strip()
                featured_image = ((news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]).strip()
                top_paragraph = (news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()).strip()
                published_date = news_soup.find("div", {"class":"article-posted-date"}).get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                sport_links.append(news_item)
            except BaseException as e:
                print(e)
        return sport_links


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