
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']  
collection = db['guncelveriler']  


result = collection.update_many(
    {},  
    {"$unset": {"conversation_date": ""}}  
)

print(f"{result.modified_count} belge güncellendi.")
