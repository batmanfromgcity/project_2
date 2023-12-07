from io import BytesIO
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
from logic import WeatherAppLogic


class WeatherAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("300x300")
        self.root.resizable(False, False)

        self.logic = WeatherAppLogic()

        # Create city label and entry
        self.city_label = tk.Label(self.root, text="City:")
        self.city_label.pack()

        self.city_entry = tk.Entry(self.root)
        self.city_entry.pack()

        # Create search button
        self.search_button = tk.Button(
            self.root, text="Search", command=self.search_weather
        )
        self.search_button.pack()

        # Create weather information labels
        self.city_info_label = tk.Label(self.root, text="")
        self.city_info_label.pack()

        self.temperature_label = tk.Label(self.root, text="")
        self.temperature_label.pack()

        self.humidity_label = tk.Label(self.root, text="")
        self.humidity_label.pack()

        self.description_label = tk.Label(self.root, text="")
        self.description_label.pack()

        # Create weather icon label
        self.weather_icon_label = tk.Label(self.root)
        self.weather_icon_label.pack()

    def search_weather(self):
        city = self.city_entry.get()
        weather_info = self.logic.get_weather(city)

        if weather_info is None:
            messagebox.showerror("Error", "Cannot find weather information.")
            return

        self.city_info_label["text"] = f"City: {weather_info['city']}"
        self.temperature_label["text"] = f"Temperature: {weather_info['temperature']:.2f}°F"
        self.humidity_label["text"] = f"Humidity: {weather_info['humidity']}%"
        self.description_label["text"] = f"Description: {weather_info['description']}"
        self.logic.save_weather_info(weather_info)

        # Load and display weather icon
        icon_url = self.get_weather_icon_url(weather_info["icon_id"])
        if icon_url:
            image = self.load_image(icon_url)
            self.weather_icon_label.configure(image=image)
            self.weather_icon_label.image = image

    def get_weather_icon_url(self, icon_id):
        return f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

    def load_image(self, url):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            image_data = response.content
            image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
            return image
        else:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherAppGUI(root)
    root.mainloop()