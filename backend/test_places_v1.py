import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:]}")

def test_new_places(destination):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.websiteUri"
    }
    data = {
        "textQuery": f"hotels in {destination}"
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        data = response.json()
        print(f"Data: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_new_places("Shimla")
