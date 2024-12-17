import requests
import bs4
import json
from nepali.date_converter import converter
import datetime
import time

class NewsScraper:
    def __init__(self, json_dir="scraper/news_data.json", date_map_dir = "scraper/date_map.json"):
        self.json_dir = json_dir
        self.date_map_dir = date_map_dir

    def __parse_nepali_date(self, website, year, month, date):
        with open(self.date_map_dir, "r") as f:
            file_data = f.read()
            data = json.loads(file_data)
        month_map = data[website]["months"]
        digit_map = data["digits"]
        parsed_month = month_map[month]
        # Convert date
        parsed_date = str()
        parsed_year = str()
        for d in date:
            parsed_date += digit_map[d]
        for y in year:
            parsed_year += digit_map[y]
        en_year, en_month, en_date = converter.nepali_to_english(int(parsed_year), parsed_month, int(parsed_date))
        # Convert to UNIX Timestamp
        date_time = datetime.datetime.timestamp(datetime.datetime(en_year, en_month, en_date))
        return date_time
    
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
    
