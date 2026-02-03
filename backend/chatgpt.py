import os
import base64
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def get_chatgpt_response(question, image_base64=None):
    if not OPENAI_API_KEY:
        return "Error: OPENAI_API_KEY not found."

    try:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

        user_content = []
        user_content.append({"type": "text", "text": question})

        if image_base64:
             # Assuming image_base64 is the raw base64 string without data prefix
             # We need to construct the data URL
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            })

        messages.append({"role": "user", "content": user_content})

        response = await client.chat.completions.create(
            model="gpt-4o", # Using GPT-4o for vision capabilities
            messages=messages,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to ChatGPT: {str(e)}"
