import os
import google.generativeai as genai

def generate_itinerary(place=None, *args, **kwargs):
    """
    Experimental itinerary generator that lists available models if it fails.
    Used for debugging model 404 errors on Render.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Gemini API key missing!"

    destination = place if place else kwargs.get("destination")
    if not destination:
        return "⚠️ No destination provided!"

    try:
        genai.configure(api_key=api_key)
        
        # Determine available models if something fails
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception as list_err:
            return f"❌ Error listing models: {str(list_err)}. Your API key might be invalid or restricted."

        # If we have models, try the first flash one or the first one in the list
        model_to_use = "gemini-1.5-flash" 
        selected_model = next((m for m in available_models if "1.5-flash" in m), None)
        if not selected_model:
            selected_model = next((m for m in available_models if "gemini-pro" in m), None)
        if not selected_model and available_models:
            selected_model = available_models[0]
            
        if not selected_model:
            return f"❌ No supported models found. Available list: {available_models}"

        # Initialize the model using the FULL name found in the list (e.g. 'models/gemini-1.5-flash')
        model = genai.GenerativeModel(selected_model)
        
        response = model.generate_content(
            f"Create a detailed 3-day travel itinerary for {destination}. Write in English."
        )
        
        if response and response.text:
            return response.text
        else:
            return f"⚠️ Empty response from {selected_model}."
            
    except Exception as e:
        return f"❌ Gemini API Error ({selected_model if 'selected_model' in locals() else 'Unknown'}): {str(e)}. Models found: {available_models}"
