import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DeepSeek API URL (compatible with OpenAI SDK)
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1" 

async def get_deepseek_response(question):
    if not DEEPSEEK_API_KEY:
        return "Error: DEEPSEEK_API_KEY not found."

    try:
        client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        
        # DeepSeek primarily focuses on text/code. Using deepseek-chat model.
        # Assuming no vision support for standard DeepSeek Chat API for this demo
        # or falling back to text only if image is provided.
        
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to DeepSeek: {str(e)}"
