#conversation_date i latest_event_time ile değiştirdiğim kod
import pymongo
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["chatbot"]
collection = db["guncelveriler"]


documents = collection.find()

for document in documents:
    
    conversation_date = document.get('conversation_date')

    if conversation_date:
        if isinstance(conversation_date, datetime): 
            latest_event_time = conversation_date
        else:
            latest_event_time = conversation_date.get('$date', None)  

        
        if latest_event_time:
            collection.update_one(
                {"_id": document["_id"]},  
                {"$set": {"latest_event_time": latest_event_time}}
            )
            print("Belge için latest_event_time başarıyla güncellendi.")
        else:
            print("Belge için geçerli bir conversation_date değeri bulunamadı.")
    else:
        print("Belge için conversation_date bulunamadı.")
