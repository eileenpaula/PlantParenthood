import json
import requests
import os
import openai
openai.organization = "org-d5FqSHnir3fX9Upv0AHqEIAa"
openai.api_key = os.environ.get('gpt_api_key')


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
                    "content": "You will be provided with a plant name, your task is to generate a dictionary with the integer number as keys and the value being a real life 7-day calender on how to take care of the plant. Assume this plant is already grown. The value must demonstrate a task that can be done once a week. Avoid mentioning daily tasks or the term once a week."
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
