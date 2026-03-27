import os
import google.generativeai as genai

def generate_itinerary(place=None, *args, **kwargs):
    """
    Robust itinerary generator for Render.
    Ensures crashes don't happen even if safety filters or API issues occur.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return "⚠️ Gemini API key is missing in your Render environment variables!"

        # Handle 'place' or 'destination' from main.py
        destination = place if place else kwargs.get("destination")
        
        if not destination:
             return "⚠️ Destination name is required to generate an itinerary."

        # Re-configure in case of environment reload
        genai.configure(api_key=api_key)

        # Using gemini-1.5-flash as it is the most modern and stable for this task
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"Create a detailed 3-day travel itinerary for {destination}. "
            f"Include daily activities and travel tips."
        )

        # Safety Check: If the response is blocked or empty
        if not response or not hasattr(response, 'text'):
            return "⚠️ Gemini API returned an empty or blocked response. Please check your safety settings or destination."

        return response.text

    except Exception as e:
        print(f"❌ Gemini Service Error: {str(e)}")
        return f"❌ FAILED TO GENERATE ITINERARY: {str(e)}. Please check your API key and connection."
