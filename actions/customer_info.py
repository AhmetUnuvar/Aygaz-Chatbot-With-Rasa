# customer_info yazısını user ile değiştiren kod
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')  
db = client['chatbot']  
collection = db['guncelveriler']  
documents = collection.find({})
for doc in documents:
    for event in doc.get('events', []):
        if event.get('event') == 'customer_input':
            
            event['event'] = 'user'
    collection.replace_one({'_id': doc['_id']}, doc)

print("Veriler başarıyla güncellendi.")
