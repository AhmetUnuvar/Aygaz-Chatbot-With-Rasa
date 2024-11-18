from pymongo import MongoClient
import time
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']
collection = db['guncelveriler']

documents = collection.find()

for document in documents:
   
    if 'dialogs' in document:
        for dialog in document.get('dialogs', []):
            timestamp = dialog.get('timestamp')  
            if timestamp:
                
                if isinstance(timestamp, datetime):
                   
                    unix_timestamp = int(time.mktime(timestamp.timetuple()))
                else:
                   
                    unix_timestamp = timestamp

               
                dialog['timestamp'] = unix_timestamp


        collection.update_one({'_id': document['_id']}, {'$set': {'dialogs': document['dialogs']}})
    else:
        print(f"Document with _id {document['_id']} does not contain 'dialogs'.")

print("Veriler başarıyla güncellendi.")
