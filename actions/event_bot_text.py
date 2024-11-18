# event : bot , user - text: "..." gruplandırmasını yaptığım kod
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']
collection = db['guncelveriler']

documents = collection.find()

for doc in documents:
    new_events = []
    
    for event in doc.get('events', []):
        new_event = {}
        
        if 'bot' in event:
            new_event["event"] = "bot"
            new_event["text"] = event["bot"]

            if 'guid' in event:
                new_event["guid"] = event["guid"]
            if 'timestamp' in event:
                new_event["timestamp"] = event["timestamp"]
            if 'sds_response_time' in event:
                new_event["sds_response_time"] = event["sds_response_time"]
            new_events.append(new_event)
        
        if 'customer_input' in event:
            new_event = {}
            new_event["event"] = "customer_input"
            new_event["text"] = event["customer_input"]
            if 'guid' in event:
                new_event["guid"] = event["guid"]
            if 'timestamp' in event:
                new_event["timestamp"] = event["timestamp"]
            if 'sds_response_time' in event:
                new_event["sds_response_time"] = event["sds_response_time"]
            new_events.append(new_event)

    collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {"events": new_events}}
    )
print("Veri formatı başarıyla güncellendi.")
