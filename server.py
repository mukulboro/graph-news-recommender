from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from recommendation.recommendation import Recommender

app = FastAPI()

class Category(BaseModel):
    news_list: List[str]

class Preference(BaseModel):
    breaking: Category
    national: Category
    intl: Category
    sports: Category
    finance: Category
    entertainment: Category
    

@app.post("/get-news")
async def get_news(
    preferences:Preference,
    ):

    prefs = {
        "breaking":{
            "news_list": preferences.breaking.news_list
        },
        "national":{
            "news_list": preferences.national.news_list
        },
        "intl":{
            "news_list": preferences.intl.news_list
        },
        "sports":{
            "news_list": preferences.sports.news_list
        },
        "finance":{
            "news_list": preferences.finance.news_list
        },
        "entertainment":{
            "news_list": preferences.entertainment.news_list
        } 
    }
    rec = Recommender(user_pref=prefs)
    all_news = rec.get_all_news()
    return all_news