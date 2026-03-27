import os
import google.generativeai as genai

def generate_itinerary(place=None, *args, **kwargs):
    """
    Robust itinerary generator with better error reporting to diagnose 404s.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ Gemini API key missing in environment variables!"

        destination = place if place else kwargs.get("destination")
        if not destination:
             return "⚠️ No destination provided!"

        genai.configure(api_key=api_key)

        # We will try a few model variations that are known to work.
        # Sometimes 'gemini-1.5-flash' works, sometimes 'gemini-1.5-flash-latest'.
        # If both fail, we list what IS available to help you fix it.
        models_to_try = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
        
        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"Create a detailed 3-day travel itinerary for {destination}",
                    # Set a timeout/request limit to fail fast
                    request_options={"timeout": 60}
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                print(f"⚠️ Model {model_name} failed: {last_error}")
                continue

        # If all tried models failed, we list the actual models your key has access to.
        try:
            all_models = [m.name for m in genai.list_models()]
            return (f"❌ ERROR: Your API key doesn't seem to have access to standard Gemini models. "
                    f"Available models for your key: {all_models}. "
                    f"Last error was: {last_error}")
        except Exception as list_err:
            return (f"❌ ERROR: Your API key might be invalid or not have the Generative Language API enabled. "
                    f"Details: {last_error}. (ListModels Error: {str(list_err)})")

    except Exception as e:
        return f"❌ FAILED: {str(e)}"
