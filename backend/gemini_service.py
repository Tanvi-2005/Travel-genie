import os
import google.generativeai as genai

def generate_itinerary(place=None, *args, **kwargs):
    """
    Experimental itinerary generator that uses the dynamically discovered model names.
    Since we found gemini-2.0-flash and gemini-flash-latest in the list, we will use those.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ Gemini API key missing!"

        destination = place if place else kwargs.get("destination")
        if not destination:
             return "⚠️ No destination provided!"

        genai.configure(api_key=api_key)

        # We'll use the specific model names we found in your account's 'list_models()' output.
        # Priority: 2.0-flash (stable) -> flash-latest -> first available in the list.
        models_to_try = [
            'gemini-2.0-flash', 
            'gemini-flash-latest', 
            'gemini-1.5-flash' # Just in case it was missed
        ]
        
        last_error = ""
        for model_name in models_to_try:
            try:
                # Some versions of the API need 'models/' prefix, some don't.
                # We'll try the name directly since it worked for list_models.
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"Create a 3-day travel itinerary for {destination}",
                    request_options={"timeout": 30}
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                # Try with 'models/' prefix just in case it was stripped
                try:
                    full_name = f"models/{model_name}"
                    model = genai.GenerativeModel(full_name)
                    response = model.generate_content(
                        f"Create a 3-day travel itinerary for {destination}",
                        request_options={"timeout": 30}
                    )
                    if response and response.text:
                        return response.text
                except Exception as e2:
                    last_error = str(e2)
                    continue

        return f"❌ FAILED: Your API key supports models like {models_to_try}, but they all failed with: {last_error}"

    except Exception as e:
        return f"❌ FAILED: {str(e)}"
