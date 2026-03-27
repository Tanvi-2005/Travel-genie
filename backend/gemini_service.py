import os
import google.generativeai as genai

def generate_itinerary(place=None, *args, **kwargs):
    """
    Simplified itinerary generator to match Render deployment requirements.
    Uses 'place' or 'destination' argument for compatibility with main.py.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Gemini API key missing in environment variables!"

    # Use 'place' if provided, otherwise check kwargs for 'destination'
    destination = place if place else kwargs.get("destination")
    
    if not destination:
        return "⚠️ No destination/place provided!"

    # Configure Gemini API inside the function to ensure the key is loaded correctly on Render
    try:
        genai.configure(api_key=api_key)
        
        # Use the most stable and widely available model 'gemini-1.5-flash'
        # The prefix 'models/' is usually added automatically by the library, 
        # but the 404 error suggests it might be missing or incorrect for some versions.
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(
            f"Create a detailed 3-day travel itinerary for {destination}. Write in the language of the request."
        )
        
        if response and response.text:
            return response.text
        else:
            return "⚠️ Received empty response from Gemini API."
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Gemini Error: {error_msg}")
        return f"❌ Gemini API Error: {error_msg}. Please check if your API key is valid for Gemini (Google AI Studio)."
