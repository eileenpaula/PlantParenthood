import pprint
import requests
# response = requests.get('https://api.unsplash.com/search/photos?page=1&query=sunflower&client_id=2THIa3M8t-GT_nc2WpNG9IeQtjjY_P32rDJM36neBOg')
# pprint.pprint(response.json())
import os
api_key = '2THIa3M8t-GT_nc2WpNG9IeQtjjY_P32rDJM36neBOg'


class Plant_image:

    def __init__(self, name):
        self.name = name

    def image(self):
        try:
            response = requests.get('https://api.unsplash.com/search/photos?page=1&query={}&client_id={}'
                                    .format(self.name, api_key))
            response.raise_for_status()  # Raise an exception for non-200 status codes

            # Parse the JSON data
            data = response.json()
            pprint.pprint(data['results'][0]['urls']['raw'])
            # Extract the image URL
            raw_image_url = data['results'][0]['urls']['raw']
            # Print the image URL
            return raw_image_url
        except requests.exceptions.RequestException as e:
            print("Error: Unable to fetch data from the API. Reason:", str(e))
        except KeyError as e:
            print("Error: Unexpected response format from the API. Reason:", str(e))

# plant = Plant_image('sunflower')
# plant.image()
