import requests

class WeatherAssistant:
    def __init__(self, api_key):
        self.base_url = "http://api.weatherapi.com/v1"
        self.api_key = api_key

    def get_weather(self, location: str):
        url = f"{self.base_url}/current.json?key={self.api_key}&q={location}"
        response = requests.get(url)
        data = response.json()
        return f"{location} weather: {data['current']['temp_c']}°C, {data['current']['condition']['text']}"