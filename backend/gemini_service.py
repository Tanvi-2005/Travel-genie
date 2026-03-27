import os
import google.generativeai as genai

def generate_itinerary(place, *args, **kwargs):
    """
    Simplified itinerary generator to match Render deployment requirements.
    Uses destination (place) and ignores extra arguments for compatibility.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Gemini API key missing!"

    genai.configure(api_key=api_key)

    # Use 'gemini-1.5-flash' for better performance/reliability if 'gemini-pro' is problematic,
    # but sticking to 'gemini-pro' as requested in the template.
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(
        f"Create a detailed 3-day travel itinerary for {place}"
    )

    return response.text
