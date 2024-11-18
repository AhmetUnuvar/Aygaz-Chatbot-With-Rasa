# mongodb de bulunan verileri istenilen formata çevirmek için kullandığım kod
from pymongo import MongoClient
import re  # regular expressions 


client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
collection = db["guncelveriler"]


def format_data(document):
    
    infonun = document.get("info", {})
    
    phone_number = None
    if isinstance(infonun, dict) and "<MOBILE_PHONE>" in infonun:
        
        phone_number_match = re.search(r"(\d{3} \d{3} \d{2} \d{2})", infonun["<MOBILE_PHONE>"])
        if phone_number_match:
            phone_number = phone_number_match.group(1)
            document["slots"]["mobile_phone"] = phone_number
            infonun["<MOBILE_PHONE>"] = ""

  
    yeni_format = {
        "_id": document.get("_id"),
        "sender_id": document.get("sender_id", "f4bca6b2-9e9f-4bc2-a8d5-8c2083dd86b8"),
        "active_loop": {
            "name": document.get("active_loop", {}).get("name", ""),
            "is_interrupted": document.get("active_loop", {}).get("is_interrupted", False),
            "rejected": document.get("active_loop", {}).get("rejected", False),
            "trigger_message": document.get("active_loop", {}).get("trigger_message", {})
        },
        "events": document.get("events", []),  
        "followup_action": document.get("followup_action", None),
        "latest_action": {
            "action_name": document.get("latest_action", {}).get("latest_action_name", "action_listen")
        },
        "latest_action_name": document.get("latest_action_name", "action_listen"),
        "latest_event_time": document.get("latest_event_time", None),
        "latest_input_channel": document.get("latest_input_channel", "rest"),
        "latest_message": document.get("latest_message", {}),
        "paused": document.get("paused", False),
        "slots": {
            "error_counter": document.get("slots", {}).get("error_counter", 0),
            "confirm_counter": document.get("slots", {}).get("confirm_counter", 0),
            "mobile_phone": phone_number,  #  telefon numarası burada olacak
            "tani_error": document.get("slots", {}).get("tani_error", None),
            "redirect": document.get("slots", {}).get("redirect", False),
            "end_flag": document.get("slots", {}).get("end_flag", False),
            "card_or_phone": document.get("slots", {}).get("card_or_phone", None),
            "card_number": document.get("slots", {}).get("card_number", None),
            "confirm_card_number": document.get("slots", {}).get("confirm_card_number", None),
            "plate": document.get("slots", {}).get("plate", None),
            "confirm_plate": document.get("slots", {}).get("confirm_plate", None),
            "requested_slot": document.get("slots", {}).get("requested_slot", "card_or_phone"),
            "session_started_metadata": document.get("slots", {}).get("session_started_metadata", None)
        }
    }

    if not yeni_format["events"]:
        yeni_format["events"] = [{
            "event": None,
            "timestamp": document.get("latest_event_time", None),
            "metadata": None,  
            "name": "action_session_start",
            "policy": None,
            "confidence": 1,
            "action_text": None,
            "hide_rule_turn": False
        }]

    if "dialogs" in document:
        yeni_format["dialogs"] = []
        for dialog in document["dialogs"]:
            dialog_copy = dialog.copy()
            if "sds_response" in dialog_copy:
                dialog_copy["bot"] = dialog_copy.pop("sds_response")
            yeni_format["dialogs"].append(dialog_copy)

   
    yeni_format["info"] = infonun 

    return yeni_format
for doc in collection.find():
    yeni_doc = format_data(doc)
    collection.update_one({"_id": doc["_id"]}, {"$set": yeni_doc})

print("Tüm veriler güncellendi.")
