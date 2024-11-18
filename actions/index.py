import pymongo
import pandas as pd
from datetime import datetime

def get_conversation_by_sender(sender_id: str):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["chatbot"]
    collection = db["aygazuserinfos"]
    conversation = collection.find_one({"sender_id": sender_id})

    if not conversation:
        return "Konuşma bulunamadı."

   
    events = conversation.get("events", [])
    conversation_dates = [
        {"timestamp": datetime.fromtimestamp(event["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
         "event_type": event["event"],
         "text": event.get("text", "")}  # Mesaj içeriğini al
        for event in events if "timestamp" in event
    ]
    
    slot_values = {slot: value for slot, value in conversation.get("slots", {}).items() if value is not None}
    
    df_dates = pd.DataFrame(conversation_dates)
    slot_data = {
        "sender_id": sender_id,
        **slot_values 
    }
    df_slots = pd.DataFrame([slot_data])  

    
    final_df = pd.concat([df_slots, df_dates], axis=1)
    
    final_df = final_df.dropna()  
    return final_df


sender_id = "430daffc0d1c4602822d188e4a226cdc"
df = get_conversation_by_sender(sender_id)
print(df.to_string())  
