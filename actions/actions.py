# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
#
#
     
class ActionGetDiseasesInformation(Action):
    def name(self):
        return "action_diseases_question"

    def run(self, dispatcher, tracker, domain):
        """Get diseases question"""
        print("Inside ActionGetDiseasesInformation")
        entities = tracker.latest_message["entities"]

        with open('data.json') as dataFile:
            parsedData = json.load(dataFile)

        print("=======================entities=======================")
        print(entities)

        result = list(map(lambda x: {"entity": x["entity"].lower(), "value": x["value"].lower()}, entities))  
        
        # get selected button from slots
        #selected_content = tracker.get_slot('selected_content')

        matchingObjects = get_matching_objects(parsedData["diseasesArray"], result)

        print(matchingObjects)

        if not matchingObjects or len(matchingObjects) == 0:
            dispatcher.utter_message(text="I did not got that. Try to rephrase.")
            return []

        dispatcher.utter_message(text=matchingObjects[0]['response'])
        return []
    
def get_matching_objects(array, input_entities):
    matching_objects = []
    for obj in array:
        for entity in obj["data"]:
            if entity in input_entities:
                matching_objects.append(obj)
                break
    matching_objects.sort(key=lambda x: len([e for e in input_entities if e in x["data"]]), reverse=True)
    return matching_objects