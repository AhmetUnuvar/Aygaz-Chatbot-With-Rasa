# lasttest_event_time formatını timestamp yapan kod
import pymongo
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["chatbot"] 
collection = db["guncelveriler"] 


documents = collection.find()  

for document in documents:
    latest_event_time = document.get("latest_event_time")
    
   
    if latest_event_time:
        
        if isinstance(latest_event_time, dict) and "$date" in latest_event_time:
            latest_event_time = latest_event_time["$date"]
        
        
        if isinstance(latest_event_time, datetime):
            timestamp = int(latest_event_time.timestamp())
            
            
            result = collection.update_one(
                {"_id": document["_id"]},  
                {"$set": {"latest_event_time": timestamp}} 
            )
            
            print(f"Belge güncellendi: {document['_id']} - {timestamp}")
        else:
            print(f"Geçerli bir datetime nesnesi bulunamadı: {document['_id']}")
    else:
        print(f"latest_event_time bulunamadı, belge  için işlem yapılmadı.")

print("Bütün belgeler güncellendi.")
