import firebase_admin
from firebase_admin import credentials, firestore
from db.database import LocalDatabase
import datetime as dt


class FirebaseNews:    
    def __init__(self, private_key_dir = "firebase/firebaseServiceKey.json"):
        cred = credentials.Certificate(private_key_dir)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.local_db = LocalDatabase()
    
    def __parse_scraped(self, date_str:str)->int:
        date = date_str.split(" ")
        y, mo, d = date[0].split("-")
        h, mi, s = date[1].split(":")
        parsed_date = dt.datetime(year=int(y), month=int(mo), day=int(d),
                                  hour=int(h), minute=int(mi), second=int(s))
        return int(parsed_date.timestamp())
        
    def upload_all_news(self):
        unuploaded_clusters = self.local_db.get_all_offline_news()
        collection_ref = self.db.collection("news")
        for cluster in unuploaded_clusters:
            doc_ref = collection_ref.document(cluster["cluster"])
            existing_document = doc_ref.get()
            if existing_document.exists:
                doc_ref.update({
                    "category": cluster["category"],
                    "published": int(cluster["published"]),
                    "news": cluster["news"],
                    "scraped": self.__parse_scraped(cluster["scraped"])
                })
            else:
                doc_ref.set({
                    "category": cluster["category"],
                    "published": int(cluster["published"]),
                    "news": cluster["news"],
                    "scraped": self.__parse_scraped(cluster["scraped"])
                })
            self.local_db.update_news_in_firebase(key=cluster["cluster"])