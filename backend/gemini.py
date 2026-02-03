import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

async def get_gemini_response(question, image_data=None, mime_type=None):
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        content = [question]
        
        if image_data and mime_type:
            # Create a dict for the image blob as expected by Gemini API
            image_blob = {
                "mime_type": mime_type,
                "data": image_data 
            }
            content.append(image_blob)

        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"
