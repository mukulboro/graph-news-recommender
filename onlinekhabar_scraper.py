from scraper import NewsScraper
import bs4
import requests
import pprint

class OnlinekhabarScraper(NewsScraper):
    def __init__(self):
        super().__init__()

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
        webpages_data = self._NewsScraper__scrape_websites(links)
        all_news = dict()
        # Work on getting breaking news first
        breaking_page:bs4.BeautifulSoup = webpages_data["homepage"]
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
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                breaking_news_list.append(news_item)
            except BaseException as e:
                continue
        all_news["breaking"] = breaking_news_list

        # Work on getting business news
        business_page:bs4.BeautifulSoup = webpages_data["finance"]
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
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                business_news_list.append(news_item)
            except BaseException as e:
                continue
        all_news["finance"] = business_news_list

        # Working on entertainment news
        entertainment_page:bs4.BeautifulSoup = webpages_data["entertainment"]
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
                headline = news_soup.find("h1", {"class":"entry-title"}).get_text().strip()
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                entertainment_links.append(news_item)
            except BaseException as e:
                continue
        all_news["entertainment"] = entertainment_links

        # Working on international news
        intl_page:bs4.BeautifulSoup = webpages_data["intl"]
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
                headline = news_soup.find("h1", {"class":"entry-title"}).get_text().strip()
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                intl_links.append(news_item)
            except BaseException as e:
                continue
        all_news["intl"] = intl_links

        # Working on national news
        national_page:bs4.BeautifulSoup = webpages_data["national"]
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
                headline = news_soup.find("h1", {"class":"entry-title"}).get_text()
                featured_image = ((news_soup.find("div", {"class":"post-thumbnail"})).find("img").attrs["src"]).strip()
                top_paragraph = (news_soup.find("div", {"class":"ok18-single-post-content-wrap"}).find("p").get_text()).strip()
                news_item["description"] = top_paragraph
                news_item["title"] = headline
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                national_links.append(news_item)
            except BaseException as e:
                continue
        all_news["national"] = national_links

        # Work on Sports News

        # okv4-post-content

        return all_news
    
    def get_all_news(self):
        news_data = self._NewsScraper__load_json_data()
        onlinekhabar = self.__parse_onlinekhabar(news_data["onlinekhabar"])
        return onlinekhabar
    
if __name__ == "__main__":
    scraper = OnlinekhabarScraper()
    news = scraper.get_all_news()
    pprint.pprint(news)