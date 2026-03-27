import os
import google.generativeai as genai

def generate_itinerary(place=None, *args, **kwargs):
    """
    Final simplified itinerary generator for Render.
    Uses 'gemini-1.5-flash' as requested. 
    Handles 'place' or 'destination' for compatibility with main.py.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Gemini API key missing!"

    # Use 'place' if provided, otherwise check kwargs for 'destination'
    destination = place if place else kwargs.get("destination")
    
    if not destination:
         return "⚠️ No destination provided!"

    # Configure Gemini API inside the function to ensure the key is loaded correctly on Render
    genai.configure(api_key=api_key)

    # UPDATED: Using 'gemini-1.5-flash' which is the latest supported model
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"Create a detailed 3-day travel itinerary for {destination}"
    )

    return response.text
