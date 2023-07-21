import pprint
import requests

class Plant_image:

    def __init__(self, name):
        self.name = name

    def image(self):
        try:
            response = requests.get('https://trefle.io/api/v1/plants/search?token=03uODOStheqAJkEGY8oxxBxC9NYoZyJ63yPyLgycO1I&q={}'
                                    .format(self.name))
            response.raise_for_status()  # Raise an exception for non-200 status codes

            # Parse the JSON data
            data = response.json()
            # Extract the image URL
            image_url = data['data'][0]['image_url']

            # Print the image URL
            return image_url
        except requests.exceptions.RequestException as e:
            print("Error: Unable to fetch data from the API. Reason:", str(e))
        except KeyError as e:
            print("Error: Unexpected response format from the API. Reason:", str(e))



# plant = Plant_image('sunflower')
# print(plant.image())


