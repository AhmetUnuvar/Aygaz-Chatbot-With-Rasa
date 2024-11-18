from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Text, Any, Dict
from rasa_sdk import FormValidationAction
import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
import pymongo


client = MongoClient('mongodb://localhost:27017')
db = client['chatbot']
collection = db['aygazuserinfos']



class validate_user_name_surname_form(FormValidationAction):

    def __init__(self):
        self.attempts = 0  

    def name(self) -> str:
        return "validate_kullanici_adi_form"
    

    def validate_inform_text(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        if slot_value.lower() == "/choose_option_evet":
            dispatcher.utter_message(text="Aydınlatma metni aydınlatma metni aydınlatma metni")
            return {"inform_text": "evet okumak istiyorum"}
        
        elif slot_value.lower() == "/choose_option_hayır":
            return {"inform_text": "hayır okumak istemiyorum", "requested_slot": "full_name"}
        
        else:
            return {"repeat_order": None}
        

    def get_names_from_file(self, file_path: str) -> list:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                names = [line.strip() for line in file if line.strip()]
            return names
        return []

    def get_surnames_from_file(self, file_path: str) -> list:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                surnames = [line.strip() for line in file if line.strip()]
            return surnames
        return []

    registered_user_info = {
        "Ahmet ünüvar": {
            "address": "Konya Karatay",
            "last_order": "x ürününden 4 adet"
        },
        "Faruk sarıgül": {
            "address": "İstanbul Esenler",
            "last_order": "y ürününden 4 adet"
        },
        "Miran sarı": {
            "address": "Ankara Kızılay",
            "last_order": "z ürününden 4 adet"
        },
        "Eda yavuz": {
            "address": "İzmir Buca",
            "last_order": "x ürününden 40 adet"
        },
        "Nurşen erdoğan": {
            "address": "İstanbul Nişantaşı",
            "last_order": "y ürününden 34 adet"
        }
    }

    def validate_full_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        full_name = slot_value.strip()
        name_parts = full_name.split()

        if self.attempts >= 2:
            dispatcher.utter_message(text="Üç kez yanlış giriş yaptınız. Müşteri temsilcisine aktarıyorum.")
            self.attempts = 0 
            return {"end_flag": True, "requested_slot": None, "redirect": True}

        if len(name_parts) < 2:
            self.attempts += 1  
            return {"full_name": None}

        surname = name_parts[-1]
        user_name = " ".join(name_parts[:-1])

        if full_name in self.registered_user_info:
            address = self.registered_user_info[full_name]["address"]
            dispatcher.utter_message(text=f"{full_name} {address} adresine kayıtlısınız.")
            return {"full_name": full_name, "requested_slot": "address_confirmation"}
        else:
            self.attempts += 1  
            dispatcher.utter_message(text="İsminiz veya soyisminiz listede kayıtlı değil.")
            return {"full_name": None}
    
    def validate_address_confirmation(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        full_name = tracker.get_slot('full_name')
        last_order = self.registered_user_info[full_name]["last_order"] if full_name in self.registered_user_info else None
        #tracker.get_intent_of_latest_message()
        if slot_value.lower() == "/confirm_yes":
            dispatcher.utter_message(text="Aynı adresten devam ediliyor.")
            return {"address_confirmation": "evet", "requested_slot": "repeat_order"}
        
        elif slot_value.lower() == "/deny_no": # olumsuz intent
            dispatcher.utter_message(text="Yeni adres için müşteri temsilcisine aktarılıyorsunuz.")
            return {"address_confirmation": "hayır", "redirect": True, "requested_slot": None}
        
        else:
            return {"address_confirmation": None}

    def validate_repeat_order(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        if slot_value.lower() == "tekrarla":
            dispatcher.utter_message(text="Siparişiniz tekrar ediliyor. Bizi tercih ettiğiniz için teşekkürler.")
            return {"repeat_order": "tekrarla"}
        
        elif slot_value.lower() == "yeni sipariş":
            return {"repeat_order": "yeni sipariş", "requested_slot": "product_names"}
        
        else:
            return {"repeat_order": None}

    def validate_product_names(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        valid_products = ["x", "y", "z"]
        if slot_value.lower() in valid_products:
            return {"product_names": slot_value, "requested_slot": "product_quantity"}
        else:
            return {"product_names": None}

    def validate_product_quantity(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        try:
            quantity = int(slot_value)
            if quantity > 0:
                return {"product_quantity": quantity, "requested_slot": "confirm_order"}
            else:
                return {"product_quantity": None}
        except ValueError:
            return {"product_quantity": None}
    
    def validate_confirm_order(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        if slot_value.lower() == "onaylıyorum":
            dispatcher.utter_message(text="Siparişiniz onaylandı. Bizi tercih ettiğiniz için teşekkürler.")
            return {"confirm_order": "onaylıyorum"}
        
        elif slot_value.lower() == "onaylamıyorum":
            dispatcher.utter_message(text="Yeni sipariş oluşturma sayfasına yönlendiriliyorsunuz...")
            return { 
                "product_names": None,
                "product_quantity": None,
                "requested_slot":"product_names"
            }
                
        else:
            dispatcher.utter_message(text="Dediğinizi anlamadım. Lütfen 'onaylıyorum' veya 'onaylamıyorum' yazınız")
            return {"confirm_order": None}
