from .base_scraper import NewsScraper
import bs4
import requests
from .base_scraper import logger


class RatopatiScraper(NewsScraper):
    def __init__(self):
        super().__init__()
        logger.info("Initialized RATIPATI scraper")
        self.news_data = self._NewsScraper__load_json_data()
        self.webpages_data = self._NewsScraper__scrape_websites(self.news_data["ratopati"])

    def __parse_publication_date(self, date_str:str):
        date,month,year=date_str.split(",")[1].strip().split(" ")  # date_str: मङ्गलबार, ०२ पुस २०८१, २१ : २४
        unix_timestamp = self._NewsScraper__parse_nepali_date("ratopati",year, month, date)
        return unix_timestamp

    def __get_category_news(self,category,limit="None")->list:
        """
        Retrieves all news from the specified category and returns a list of up to the specified limit.
        If no limit is provided, it returns all news from the category.
        """
        category_page:bs4.BeautifulSoup = self.webpages_data[category]
        category_grids=category_page.find_all("div",{"class":"columnnews mbl-col col3"})
        all_category_links = [x.find("a") for x in category_grids]
        category_news_list = []
        item:bs4.element.Tag

        if limit=="None":
            limit=len(all_category_links)

        for item in all_category_links[:limit]:
            try:
                news_item = dict()
                headline_link = item.attrs["href"]
                # Extra request to get news description and image
                response = requests.get(headline_link)
                response.encoding = "utf-8"
                news_soup = bs4.BeautifulSoup(response.text, "html.parser")

                headline=news_soup.find("h2",{"class":"heading"}).get_text().strip()
                featured_image_container = news_soup.find("figure", {"class":"featured-image"})
                if featured_image_container:
                    featured_image=featured_image_container.find("img").attrs["src"].strip()
                else:
                    featured_image="https://cdn.pixabay.com/photo/2014/04/02/17/04/newspaper-307829_1280.png"
                top_paragraph = (news_soup.find("div", {"class":"the-content"}).find("p").get_text()).strip().replace("\xa0", " ")
                published_date = news_soup.find("div", {"class":"post-hour"}).find("span").get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph
                news_item["title"] = headline.replace("\xa0", " ")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                category_news_list.append(news_item)
            except BaseException as e:
                continue
   
        return category_news_list


    def __get_breaking_news(self):
        breaking_page:bs4.BeautifulSoup = self.webpages_data["homepage"]
        breaking_containers = breaking_page.find_all("div", {"class": "breaking-col text--center"})
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
                featured_image_container = news_soup.find("figure", {"class":"featured-image"})
                if featured_image_container:
                    featured_image=featured_image_container.find("img").attrs["src"].strip()
                else:
                    featured_image="https://cdn.pixabay.com/photo/2014/04/02/17/04/newspaper-307829_1280.png"
                top_paragraph = (news_soup.find("div", {"class":"the-content"}).find("p").get_text()).strip()
                published_date = news_soup.find("div", {"class":"post-hour"}).find("span").get_text().strip()
                news_item["published"] = self.__parse_publication_date(published_date)
                news_item["description"] = top_paragraph.replace("\xa0", " ")
                news_item["title"] = headline.replace("\xa0", " ")
                news_item["url"] = headline_link
                news_item["image"] = featured_image
                breaking_news_list.append(news_item)
            except BaseException as e:
                print(e)
        return breaking_news_list
    
    def __get_business_news(self)->list:
        return self.__get_category_news("finance",10)
    
    def __get_intl_news(self)->list:
        return self.__get_category_news("intl",10)
    
    def __get_entertainment_news(self):
        return self.__get_category_news("entertainment", 10)
    
    def __get_sports_news(self):
        sports_category=["sportsSpecial","npl","football","cricket"]
        sports_news_list=[]
        for category in sports_category:
            sports_news_list.extend(self.__get_category_news(category,2))
        return sports_news_list
    
    def __get_national_news(self):
        provinces_category=["koshi","madhesh","bagmati","gandaki","lumbini","karnali","sudurpashchim"]
        national_news_list=[]
        for category in provinces_category:
            national_news_list.extend(self.__get_category_news(category,2))
        return national_news_list
    
    def get_all_news(self):
        return {
            "breaking": self.__get_breaking_news(),
            "national": self.__get_national_news(),
            "intl": self.__get_intl_news(),
            "finance": self.__get_business_news(),
            "entertainment": self.__get_entertainment_news(),
            "sports": self.__get_sports_news()
        }
        