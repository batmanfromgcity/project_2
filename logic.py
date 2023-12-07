import requests
import csv


class WeatherAppLogic:
    def __init__(self):
        self.weather_key = '212aba012e6c2de238e15db161bd88a3'

    def get_weather(self, city):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"appid": self.weather_key, "q": city, "units": "metric"}
        response = requests.get(url, params=params)
        weather_data = response.json()

        if response.status_code == 200:
            temperature_celsius = weather_data["main"]["temp"]
            temperature_fahrenheit = self.convert_celsius_to_fahrenheit(temperature_celsius)
            weather_info = {
                "city": weather_data["name"],
                "temperature": temperature_fahrenheit,
                "humidity": weather_data["main"]["humidity"],
                "description": weather_data["weather"][0]["description"],
                "icon_id": weather_data["weather"][0]["icon"],
            }
            return weather_info
        else:
            return None

    @staticmethod
    def convert_celsius_to_fahrenheit(celsius):
        return celsius * 9 / 5 + 32
    
    @staticmethod
    def save_weather_info(weather_info):
        with open('weather_brief.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow(weather_info.keys())
            writer.writerow(weather_info.values())
