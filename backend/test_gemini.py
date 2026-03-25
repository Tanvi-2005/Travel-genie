import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("No GEMINI_API_KEY found in .env")
else:
    print(f"Key loaded: {key[:10]}...")
    
genai.configure(api_key=key)

try:
    print("Testing models/gemini-2.5-flash...")
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content("hello")
    print("SUCCESS:", response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
