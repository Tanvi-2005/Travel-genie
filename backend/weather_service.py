import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_weather(city: str):
    """Fetch current weather for a specific city using OpenWeatherMap API."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("⚠️ WEATHER_API_KEY is missing!")
        return None
        
    # OpenWeatherMap API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "city": data["name"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        print(f"❌ Weather API error for {city}: {e}")
        return None
