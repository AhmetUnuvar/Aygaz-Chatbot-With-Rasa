from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']  
collection = db['guncelveriler']  


documents = collection.find() 

for document in documents:
    if "dialogs" in document and isinstance(document["dialogs"], list):
        document["events"] = document["dialogs"]

        del document["dialogs"]
        
        collection.update_one({"_id": document["_id"]}, {"$set": document})
        print(f"Belge güncellendi: ")
    else:
        print(f"Belgede 'dialogs' alanı bulunamadı veya geçerli bir liste değil: ")

print("Tüm belgelerde işlem tamamlandı.")
