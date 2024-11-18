# yeni verileri sunucu üzerinden tower veritabanına aktaran kod
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
    ('193.35.200.106', 22),  
    ssh_username='hiddenslate',
    ssh_password='inoX9ghslate',
    remote_bind_address=('127.0.0.1', 27017)  
) as tunnel:
    
    local_client = MongoClient("mongodb://127.0.0.1:27017")
    local_db = local_client["chatbot"]
    local_collection = local_db["guncelveriler"]
    remote_client = MongoClient(f"mongodb://127.0.0.1:{tunnel.local_bind_port}")
    remote_db = remote_client["sds_voice"]
    remote_collection = remote_db["blacklist_target"]
    documents = list(local_collection.find())
    if documents:
        remote_collection.insert_many(documents)
        print("aktarıldı.")
    else:
        print("bulunamadı.")

local_client.close()
remote_client.close()
