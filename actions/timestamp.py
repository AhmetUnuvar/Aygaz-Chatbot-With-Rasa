# belirtilen zamanları timestamp formatına çevirdiğim kod
from pymongo import MongoClient
from datetime import datetime
import pytz

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
collection = db["guncelveriler"]


def convert_timestamp(document):
    
    dialogs = document.get("dialogs", [])
    for dialog in dialogs:
        if "timestamp" in dialog:
            timestamp = dialog["timestamp"]
            if isinstance(timestamp, str):  
               
                timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                timestamp_obj = timestamp_obj.replace(tzinfo=pytz.utc)  
               
                unix_timestamp = timestamp_obj.timestamp()
                dialog["timestamp"] = unix_timestamp

    if "conversation_date" in document:
        conversation_date = document["conversation_date"]
        if isinstance(conversation_date, str):  
            conversation_date_obj = datetime.strptime(conversation_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            conversation_date_obj = conversation_date_obj.replace(tzinfo=pytz.utc)  
            unix_conversation_date = conversation_date_obj.timestamp()
            document["conversation_date"] = unix_conversation_date
    
    return document

for doc in collection.find():
    updated_doc = convert_timestamp(doc)
    collection.update_one({"_id": doc["_id"]}, {"$set": updated_doc})

print("Tamamlandı.")
