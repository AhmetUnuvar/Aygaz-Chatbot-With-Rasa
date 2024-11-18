from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']  
collection = db['guncelveriler']  
for document in collection.find():
    update_fields = {}
    

    if "end_flag" in document:
        update_fields["slots.end_flag"] = document["end_flag"]
        update_fields["end_flag"] = ""  

    if "forward_to" in document:
        update_fields["slots.forward_to"] = document["forward_to"]
        update_fields["forward_to"] = ""  

    if update_fields:
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {k: v for k, v in update_fields.items() if k.startswith("slots.")},
             "$unset": {k: "" for k in update_fields if not k.startswith("slots.")}}
        )

print("Tüm belgeler güncellendi: 'end_flag' ve 'forward_to' alanları 'slots' içerisine taşındı.")
