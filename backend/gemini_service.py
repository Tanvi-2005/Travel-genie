import os
import google.generativeai as genai

def generate_itinerary(place=None, *args, **kwargs):
    """
    Simplified itinerary generator to match Render deployment requirements.
    Uses 'place' or 'destination' argument for compatibility with main.py.
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

    # Use 'gemini-1.5-flash' if 'gemini-pro' fails, but sticking to the requested template.
    try:
        model = genai.GenerativeModel("gemini-1.5-flash") # 1.5-flash is more stable/reliable
        response = model.generate_content(
            f"Create a detailed 3-day travel itinerary for {destination}"
        )
        return response.text
    except Exception as e:
        print(f"⚠️ Gemini 1.5 error, trying gemini-pro: {e}")
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(
                f"Create a detailed 3-day travel itinerary for {destination}"
            )
            return response.text
        except Exception as e2:
            return f"❌ Gemini API Error: {str(e2)}"
