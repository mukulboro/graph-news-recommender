import firebase_admin
from firebase_admin import credentials, firestore
from db.database import LocalDatabase

class FirebaseNews:    
    def __init__(self, private_key_dir = "firebase/firebaseServiceKey.json"):
        cred = credentials.Certificate(private_key_dir)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.local_db = LocalDatabase()
        
    def upload_all_news(self):
        unuploaded_clusters = self.local_db.get_all_offline_news()
        collection_ref = self.db.collection("news")
        for cluster in unuploaded_clusters:
            doc_ref = collection_ref.document(cluster["cluster"])
            doc_ref.set({
                "category": cluster["category"],
                "published": int(cluster["published"]),
                "news": cluster["news"]
            })
            self.local_db.update_news_in_firebase(key=cluster["cluster"])