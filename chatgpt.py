import json
import requests
import os
import openai
openai.organization = "org-d5FqSHnir3fX9Upv0AHqEIAa"
openai.api_key = os.environ.get('gpt_api_key')

class ChatGPT:

    def __init__(self, name):
        self.name = name
    
    def careCalender(self):
        plant_name = self.name
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a plant name, your task is to generate a dictionary of length 30 with the days as keys of a real-life 30-days calender with insturctions on how to take care of the plant. Assume the plant is already grown"
                },
                {
                    "role": "user",
                    "content": "Plant Name: " + plant_name
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )
        result = response["choices"][0]["message"]["content"]
        return(result)

sunflower = ChatGPT("Sunflower")
print(sunflower.careCalender())