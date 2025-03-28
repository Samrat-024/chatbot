from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionCheckOut(Action):
    def name(self):
        return "action_check_out"

    def run(self, dispatcher, tracker, domain):
        room_number = tracker.get_slot("room_number")
        guest_name = tracker.get_slot("guest_name")

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

        return [SlotSet("room_number", None), SlotSet("guest_name", None)]
