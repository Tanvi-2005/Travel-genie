"""
Gemini AI Service for generating personalized travel itineraries.
Uses Google's Generative AI (Gemini) API.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()



def configure_gemini():
    """Configure the Gemini API with the provided key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("⚠️ GEMINI_API_KEY is missing or invalid in environment variables!")
        return False
    
    try:
        print(f"✅ Configuring Gemini with key starting with: {api_key[:5]}...")
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"❌ Failed to configure Gemini API: {e}")
        return False


def generate_itinerary(destination: str, budget: float, duration_days: int,
                       travel_style: str, interests: str = "",
                       ml_recommendation: str = "", language: str = "English",
                       people: int = 1,
                       start_date: str = "", end_date: str = "",
                       weather_info: str = "") -> str:
    """
    Generate a personalized travel itinerary using Gemini AI.
    
    Args:
        destination: Target destination
        budget: Trip budget in USD
        duration_days: Number of days for the trip
        travel_style: Style (adventure, relaxation, cultural, family)
        interests: User's specific interests
        ml_recommendation: ML-predicted destination category
    
    Returns:
        Generated itinerary string from Gemini
    """
    if not configure_gemini():
        return _generate_fallback_itinerary(destination, budget, duration_days, travel_style, interests, ml_recommendation, language, people, start_date, end_date)

    weather_text = f"\n- Current Weather at Destination: {weather_info}" if weather_info else ""
    
    prompt = f"""You are Travel Genie, an expert AI travel planner for India. Create a detailed, personalized travel itinerary.

**Trip Details:**
- Traveller: {destination} trip for an Indian traveller
- Group Size: {people} people
- Budget: ₹{budget:,.0f} INR (Indian Rupees)
- Dates: {start_date} to {end_date} (Duration: {duration_days} days)
- Travel Style: {travel_style}
- Interests: {interests if interests else "General sightseeing"}
- AI Recommended Category: {ml_recommendation}{weather_text}

**Generate a complete day-by-day itinerary that includes:**
1. Day-wise itinerary with morning, afternoon, and evening activities
2. Recommended restaurants and local cuisine to try
3. Estimated costs for major activities in Indian Rupees (₹)
4. Travel tips, insider tips and hidden gems
5. Transportation suggestions (trains, buses, autos, cabs within India)
6. Accommodation recommendations within budget (in ₹)
7. Safety tips and cultural etiquette
8. Best places to visit and suggested activities specific to the destination
9. Recommendations and packing tips based on the current weather condition

All costs MUST be in Indian Rupees (₹). Format the response with clear day headers and bullet points. Make it engaging and practical for Indian travellers.
** IMPORTANT: The entire response MUST be written in the {language} language. **
"""

    try:
        # Use stable gemini-1.5-flash as primary for reliability
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        if not response or not response.text:
            raise ValueError("Empty response from Gemini 1.5")
        return response.text
    except Exception as e:
        print(f"⚠️ Gemini 1.5 error: {e}")
        try:
            # Attempt experimental backup
            print("🔄 Attempting backup with gemini-2.0-flash-exp...")
            model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
            response = model.generate_content(prompt)
            if not response or not response.text:
                raise ValueError("Empty response from Gemini 2.0")
            return response.text
        except Exception as e2:
            print(f"❌ Gemini API Error (Primary and Backup failed): {e2}")
            # The UI will show this fallback itinerary
            return _generate_fallback_itinerary(destination, budget, duration_days, travel_style, interests, ml_recommendation, language, people, start_date, end_date)


def _generate_fallback_itinerary(destination, budget, duration_days, travel_style, interests, ml_recommendation, language, people, start_date, end_date):
    """Generate a basic fallback itinerary when Gemini API is unavailable."""
    daily_budget = budget / duration_days if duration_days > 0 else budget

    # Translations for fallback
    translations = {
        "English": {
            "title": "Travel Genie Itinerary", "budget": "Budget", "duration": "Duration", "days_txt": "days",
            "style": "Style", "daily": "Daily Budget", "ai_cat": "AI Category", "destination": "destination",
            "day": "Day", "morning": "Morning", "afternoon": "Afternoon", "evening": "Evening", "acc": "Accommodation",
            "morning_txt": "Explore local spots and begin with", "afternoon_txt": f"Visit popular {destination} attractions and try local cuisine",
            "evening_txt": "Enjoy dinner at a recommended restaurant and evening entertainment", "acc_txt": "Budget-friendly stay",
            "night": "night", "tips_h": "Tips", "tips_txt": "Book accommodations in advance, try street food for authentic experiences, and always carry local currency.",
            "note": "Note: This is a basic itinerary. Add your Gemini API key for AI-powered detailed planning!",
            "adv": ['hiking trails', 'zip-lining', 'water sports', 'rock climbing', 'paragliding'],
            "rel": ['spa treatments', 'beach lounging', 'sunset cruises', 'yoga retreats', 'hot springs'],
            "cul": ['museum tours', 'historical landmarks', 'local cooking classes', 'art galleries', 'temple visits'],
            "fam": ['theme parks', 'zoo visits', 'boat rides', 'nature walks', 'interactive museums']
        },
        "Hindi": {
            "title": "ट्रेवल जिन्न इटिनरेरी", "budget": "बजट", "duration": "अवधि", "days_txt": "दिन",
            "style": "शैली", "daily": "दैनिक बजट", "ai_cat": "AI श्रेणी", "destination": "गंतव्य",
            "day": "दिन", "morning": "सुबह", "afternoon": "दोपहर", "evening": "शाम", "acc": "आवास",
            "morning_txt": "स्थानीय स्थानों का अन्वेषण करें और शुरुआत करें", "afternoon_txt": f"{destination} के लोकप्रिय आकर्षण स्थलों की यात्रा करें और स्थानीय भोजन का आनंद लें",
            "evening_txt": "अनुशंसित रेस्तरां में रात के खाने और मनोरंजन का आनंद लें", "acc_txt": "बजट के अनुकूल प्रवास",
            "night": "रात", "tips_h": "सुझाव", "tips_txt": "आवास पहले से बुक करें, प्रामाणिक अनुभवों के लिए स्ट्रीट फूड आज़माएं, और हमेशा स्थानीय मुद्रा साथ रखें।",
            "note": "नोट: यह एक बुनियादी कार्यक्रम है। AI-संचालित विस्तृत योजना के लिए अपनी जेमिनी API कुंजी (API key) जोड़ें!",
            "adv": ['हाइकिंग ट्रेल्स', 'ज़िप-लाइनिंग', 'वाटर स्पोर्ट्स', 'रॉक क्लाइम्बिंग', 'पैराग्लाइडिंग'],
            "rel": ['स्पा उपचार', 'बीच लाउंजिंग', 'सनसेट क्रूज़', 'योग रिट्रीट', 'गर्म झरने'],
            "cul": ['संग्रहालय भ्रमण', 'ऐतिहासिक स्थल', 'स्थानीय कुकिंग क्लासेस', 'आर्ट गैलरी', 'मंदिर दर्शन'],
            "fam": ['थीम पार्क', 'चिड़ियाघर की सैर', 'नाव की सवारी', 'पार्क वॉक', 'इंटरैक्टिव संग्रहालय']
        },
        "Punjabi": {
            "title": "ਟਰੈਵਲ ਜਿੰਨੀ ਇਟਿਨਰਰੀ", "budget": "ਬਜਟ", "duration": "ਅਵਧੀ", "days_txt": "ਦਿਨ",
            "style": "ਸ਼ੈਲੀ", "daily": "ਰੋਜ਼ਾਨਾ ਬਜਟ", "ai_cat": "AI ਸ਼੍ਰੇਣੀ", "destination": "ਮੰਜ਼ਿਲ",
            "day": "ਦਿਨ", "morning": "ਸਵੇਰ", "afternoon": "ਦੁਪਹਿਰ", "evening": "ਸ਼ਾਮ", "acc": "ਰਿਹਾਇਸ਼",
            "morning_txt": "ਸਥਾਨਕ ਥਾਵਾਂ ਦੀ ਪੜਚੋਲ ਕਰੋ ਅਤੇ ਇਸ ਨਾਲ ਸ਼ੁਰੂ ਕਰੋ", "afternoon_txt": f"{destination} ਦੇ ਪ੍ਰਸਿੱਧ ਆਕਰਸ਼ਣ ਦੇਖੋ ਅਤੇ ਸਥਾਨਕ ਭੋਜਨ ਦਾ ਅਨੰਦ ਲਓ",
            "evening_txt": "ਸਿਫ਼ਾਰਿਸ਼ ਕੀਤੇ ਰੈਸਟੋਰੈਂਟ ਵਿੱਚ ਰਾਤ ਦੇ ਖਾਣੇ ਅਤੇ ਮਨੋਰੰਜਨ ਦਾ ਅਨੰਦ ਲਓ", "acc_txt": "ਬਜਟ-ਅਨੁਕੂਲ ਠਹਿਰਨ",
            "night": "ਰਾਤ", "tips_h": "ਸੁਝਾਅ", "tips_txt": "ਰਿਹਾਇਸ਼ ਦੀ ਪੇਸ਼ਗੀ ਬੁਕਿੰਗ ਕਰੋ, ਪ੍ਰਮਾਣਿਕ ਅਨੁਭਵਾਂ ਲਈ ਸਟ੍ਰੀਟ ਫੂਡ ਅਜ਼ਮਾਓ, ਅਤੇ ਹਮੇਸ਼ਾ ਸਥਾਨਕ ਕਰੰਸੀ ਨਾਲ ਰੱਖੋ।",
            "note": "ਨੋਟ: ਇਹ ਇੱਕ ਬੁਨਿਆਦੀ ਇਟਿਨਰਰੀ ਹੈ। AI-ਸੰਚਾਲਿਤ ਵਿਸਤ੍ਰਿਤ ਯੋਜਨਾਬੰਦੀ ਲਈ ਆਪਣੀ Gemini API ਕੁੰਜੀ (API key) ਸ਼ਾਮਲ ਕਰੋ!",
            "adv": ['ਹਾਈਕਿੰਗ ਟਰੇਲਜ਼', 'ਜ਼ਿਪ-ਲਾਈਨਿੰਗ', 'ਵਾਟਰ ਸਪੋਰਟਸ', 'ਰਾਕ ਕਲਾਈਮਬਿੰਗ', 'ਪੈਰਾਗਲਾਈਡਿੰਗ'],
            "rel": ['ਸਪਾ ਇਲਾਜ', 'ਬੀਚ ਲਾਉਂਜਿੰਗ', 'ਸਨਸੈਟ ਕਰੂਜ਼', 'ਯੋਗਾ ਰਿਟਰੀਟ', 'ਗਰਮ ਝਰਨੇ'],
            "cul": ['ਅਜਾਇਬ ਘਰਾਂ ਦੇ ਦੌਰੇ', 'ਇਤਿਹਾਸਕ ਸਥਾਨ', 'ਸਥਾਨਕ ਕੁਕਿੰਗ ਕਲਾਸਾਂ', 'ਆਰਟ ਗੈਲਰੀਆਂ', 'ਮੰਦਰ ਦਰਸ਼ਨ'],
            "fam": ['ਥੀਮ ਪਾਰਕਸ', 'ਚਿੜੀਆਘਰ ਦੇ ਦੌਰੇ', 'ਕਿਸ਼ਤੀ ਦੀ ਸਵਾਰੀ', 'ਪਾਰਕ ਵਾਕ', 'ਇੰਟਰਐਕਟਿਵ ਅਜਾਇਬ ਘਰ']
        },
        "Kannada": {
            "title": "ಇಟಿನೆರರಿ (ವೇಳಾಪಟ್ಟಿ)", "budget": "ಬಜೆಟ್", "duration": "ಅವಧಿ", "days_txt": "ದಿನಗಳು",
            "style": "ಶೈಲಿ", "daily": "ದೈನಂದಿನ ಬಜೆಟ್", "ai_cat": "AI ವರ್ಗ", "destination": "ಗಮ್ಯಸ್ಥಾನ",
            "day": "ದಿನ", "morning": "ಬೆಳಿಗ್ಗೆ", "afternoon": "ಮಧ್ಯಾಹ್ನ", "evening": "ಸಂಜೆ", "acc": "ವಸತಿ",
            "morning_txt": "ಸ್ಥಳೀಯ ತಾಣಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ಮತ್ತು ಇದರೊಂದಿಗೆ ಪ್ರಾರಂಭಿಸಿ", "afternoon_txt": f"{destination} ಜನಪ್ರಿಯ ಆಕರ್ಷಣೆಗಳನ್ನು ಭೇಟಿ ಮಾಡಿ ಮತ್ತು ಸ್ಥಳೀಯ ಆಹಾರವನ್ನು ಆನಂದಿಸಿ",
            "evening_txt": "ಶಿಫಾರಸು ಮಾಡಿದ ರೆಸ್ಟೋರೆಂಟ್‌ನಲ್ಲಿ ರಾತ್ರಿಯ ಊಟ ಮತ್ತು ಮನರಂಜನೆಯನ್ನು ಆನಂದಿಸಿ", "acc_txt": "ಬಜೆಟ್-ಸ್ನೇಹಿ ವಸತಿ",
            "night": "ರಾತ್ರಿ", "tips_h": "ಸಲಹೆಗಳು", "tips_txt": "ವಸತಿಗಳನ್ನು ಮುಂಚಿತವಾಗಿ ಕಾಯ್ದಿರಿಸಿ, ಅಧಿಕೃತ ಅನುಭವಗಳಿಗಾಗಿ ಬೀದಿಬದಿಯ ಆಹಾರವನ್ನು ಪ್ರಯತ್ನಿಸಿ ಮತ್ತು ಯಾವಾಗಲೂ ಸ್ಥಳೀಯ ಹಣವನ್ನು ಒಯ್ಯಿರಿ.",
            "note": "ಸೂಚನೆ: ಇದು ಕೇವಲ ಮೂಲ ವೇಳಾಪಟ್ಟಿಯಾಗಿದೆ. AI-ಚಾಲಿತ ವಿವರವಾದ ಯೋಜನೆಗಳಿಗಾಗಿ ನಿಮ್ಮ ಜೆಮಿನಿ API ಕೀ ಸೇರಿಸಿ!",
            "adv": ['ಚಾರಣ', 'ಜಿಪ್-ಲೈನಿಂಗ್', 'ವಾಟರ್ ಸ್ಪೋರ್ಟ್ಸ್', 'ರಾಕ್ ಕ್ಲೈಂಬಿಂಗ್', 'ಪ್ಯಾರಾಗ್ಲೈಡಿಂಗ್'],
            "rel": ['ಸ್ಪಾ ಚಿಕಿತ್ಸೆಗಳು', 'ಬೀಚ್ ಲೌಂಜಿಂಗ್', 'ಸನ್ಸೆಟ್ ಕ್ರೂಸಸ್', 'ಯೋಗಾಭ್ಯಾಸ', 'ಬಿಸಿನೀರಿನ ಬುಗ್ಗೆಗಳು'],
            "cul": ['ವಸ್ತುಸಂಗ್ರಹಾಲಯ ಪ್ರವಾಸಗಳು', 'ಐತಿಹಾಸಿಕ ಹೆಗ್ಗುರುತುಗಳು', 'ಸ್ಥಳೀಯ ಅಡುಗೆ ತರಗತಿಗಳು', 'ಆರ್ಟ್ ಗ್ಯಾಲರಿಗಳು', 'ದೇವಾಲಯ ಭೇಟಿಗಳು'],
            "fam": ['ಥೀಮ್ ಪಾರ್ಕ್‌ಗಳು', 'ಮೃಗಾಲಯ ಭೇಟಿಗಳು', 'ದೋಣಿ ಸವಾರಿ', 'ಪಾರ್ಕ್ ವಾಕ್', 'ಸಂವಾದಾತ್ಮಕ ವಸ್ತುಸಂಗ್ರಹಾಲಯಗಳು']
        }
    }

    t = translations.get(language, translations["English"])

    style_key = "cul"
    if travel_style == "adventure": style_key = "adv"
    elif travel_style == "relaxation": style_key = "rel"
    elif travel_style == "family": style_key = "fam"

    activities = t[style_key]

    itinerary = f"# 🌍 {t['title']}: {destination}\n\n"
    itinerary += f"**{t['budget']}:** ₹{budget:,.0f} | **Dates:** {start_date} to {end_date} | **{t['style']}:** {travel_style.title()}\n"
    itinerary += f"**{t['daily']}:** ~₹{daily_budget:,.0f}/{t['days_txt']}\n"
    if ml_recommendation:
        itinerary += f"**{t['ai_cat']}:** {ml_recommendation.title()} {t['destination']}\n"
    itinerary += "\n---\n\n"

    for day in range(1, duration_days + 1):
        activity_idx = (day - 1) % len(activities)
        itinerary += f"## {t['day']} {day}\n\n"
        itinerary += f"🌅 **{t['morning']}:** {t['morning_txt']} {activities[activity_idx]}\n"
        itinerary += f"☀️ **{t['afternoon']}:** {t['afternoon_txt']} (~₹{daily_budget * 0.3:,.0f})\n"
        itinerary += f"🌙 **{t['evening']}:** {t['evening_txt']} (~₹{daily_budget * 0.3:,.0f})\n"
        itinerary += f"🏨 **{t['acc']}:** {t['acc_txt']} (~₹{daily_budget * 0.4:,.0f}/{t['night']})\n\n"

    itinerary += "---\n\n"
    itinerary += f"💡 **{t['tips_h']}:** {t['tips_txt']}\n"
    itinerary += f"\n⚠️ *{t['note']}*"

    return itinerary
