import json
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import openai
openai.organization = "org-a7U4QMb1bOxH31funt61Aon9"
openai.api_key = os.getenv('gpt_api_key')

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
    