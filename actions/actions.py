from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import requests

class ActionCheckOut(Action):
    def name(self):
        return "action_check_out"

    def run(self, dispatcher, tracker, domain):
        room_number = tracker.get_slot("room_number")
        guest_name = tracker.get_slot("guest_name")

        rails_api_url = 'http://127.0.0.1:3000/api/v1/checkins/checkout'

        if not room_number and not guest_name:
            dispatcher.utter_message(text="Please provide both the guest's name and room number to check out.")
            return []
        elif not room_number:
            dispatcher.utter_message(text="Please provide a room number to check out.")
            return []
        elif not guest_name:
            dispatcher.utter_message(text=f"Who should I check out from room {room_number}?")
            return []
        
        formatted_guest_name = guest_name.title()
        dispatcher.utter_message(text=f"Checking out guest {formatted_guest_name} from room {room_number} ✅")

        payload = {
            "guest_name": formatted_guest_name,
            "room_number": room_number,
        }

        try:
            response = requests.put(rails_api_url, json=payload)
            response.raise_for_status()

            if response.status_code == 200:
                dispatcher.utter_message(text=f"Successfully checked out guest {formatted_guest_name} from room {room_number} ✅")
            else:
                dispatcher.utter_message(text=f"Failed to check out guest {formatted_guest_name} from room {room_number}. Please try again.")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"An error occurred while checking out the guest: {e}")

        return [SlotSet("room_number", None), SlotSet("guest_name", None)]


class ActionCheckIn(Action):
    def name(self):
        return "action_check_in"
    
    def run(self, dispatcher, tracker, domain):
        room_number = tracker.get_slot("room_number")
        guest_name = tracker.get_slot("guest_name")

        checkin_api = 'http://127.0.0.1:3000/api/v1/checkins'

        if not room_number and not guest_name:
            dispatcher.utter_message(text="Please provide both the guest's name and room number to check in.")
            return []
        elif not room_number:
            dispatcher.utter_message(text="Please provide a room number to check in.")
            return []
        elif not guest_name:
            dispatcher.utter_message(text=f"Who should I check in to room {room_number}?")
            return []
        
        formatted_guest_name = guest_name.title()
        dispatcher.utter_message(text=f"Checking in guest {formatted_guest_name} to room {room_number} ✅")

        payload = {
            "guest_name": formatted_guest_name,
            "room_number": room_number,
        }

        try:
            response = requests.post(checkin_api, json=payload)  
            response.raise_for_status()

            if response.status_code == 201:  
                dispatcher.utter_message(text=f"Successfully checked in guest {formatted_guest_name} to room {room_number} ✅")
            else:
                dispatcher.utter_message(text=f"Failed to check in guest {formatted_guest_name} to room {room_number}. Please try again.")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"An error occurred while checking in the guest: {e}")

        return [SlotSet("room_number", None), SlotSet("guest_name", None)]
