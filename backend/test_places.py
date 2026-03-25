import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:]}")

def test_hotels(destination):
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"best budget friendly hotels in {destination}",
        "key": API_KEY,
        "type": "lodging"
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    print(f"Status: {data.get('status')}")
    if data.get("status") == "OK":
        for res in data.get("results")[:2]:
            print(f"- {res.get('name')}")
    else:
        print(f"Error: {data.get('error_message')}")

if __name__ == "__main__":
    test_hotels("Shimla")
