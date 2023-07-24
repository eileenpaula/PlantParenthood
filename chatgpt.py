import json
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import openai
openai.organization = "org-d5FqSHnir3fX9Upv0AHqEIAa"
#openai.api_key1 = os.environ.get('gpt_api_key')
openai.api_key= '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'

class ChatGPT:

    def __init__(self, name):
        self.name = name

    def careCalendar(self):
        plant_name = self.name
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a plant name, your task is to generate a dictionary with the integer number as keys of a real-life 30-days calender starting with today's date with insturctions on how to take care of the plant. Assume the plant is already grown"
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

    def info(self):
        plant_name = self.name
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a plant name. Your task is to generate a dictionary with detailed information about the plant, including its description, preferred growing conditions (indoor/outdoor/either), plant type, climate, soil type, watering, and fun facts. Assume the plant is already grown."
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
        return result

    def is_plant(self):
        plant_name = self.name
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with an object name. Your task is to return a true or false value on whether the object is a plant."
                },
                {
                    "role": "user",
                    "content": "object Name: " + plant_name
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )
        result = response["choices"][0]["message"]["content"]
        return result

# test = ChatGPT('sunflower')
# print(test.info())


