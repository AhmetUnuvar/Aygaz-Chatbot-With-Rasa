from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder

ssh_host = '193.35.200.106'
ssh_username = 'hiddenslate'
ssh_password = 'inoX9ghslate'
ssh_port = 22

remote_db = 'sds_voice'
remote_collection_name = 'blacklist_test'
local_db = 'chatbot'
local_collection_name = 'guncelveriler'

with SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_username,
    ssh_password=ssh_password,
    remote_bind_address=('localhost', 27017)
) as tunnel:
    client_remote = MongoClient(f'mongodb://127.0.0.1:{tunnel.local_bind_port}')
    remote_db_instance = client_remote[remote_db]
    remote_collection = remote_db_instance[remote_collection_name]
    
    client_local = MongoClient('mongodb://localhost:27017')
    local_db_instance = client_local[local_db]
    local_collection = local_db_instance[local_collection_name]
    
    remote_data = remote_collection.find()
    
    local_collection.insert_many(remote_data)

    client_remote.close()
    client_local.close()


            
