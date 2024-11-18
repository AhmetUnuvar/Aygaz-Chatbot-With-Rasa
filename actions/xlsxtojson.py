from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]  
collection = db["surnames"]  


with open('turkish_surnames.txt', 'r', encoding='utf-8') as file:
    for line in file:
        name = line.strip()  
        if name:  
            
            collection.insert_one({"surname": name})

print("İsimler başarıyla MongoDB'ye eklendi.")