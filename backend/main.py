from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio
import base64

from backend.chatgpt import get_chatgpt_response
from backend.gemini import get_gemini_response
from backend.deepseek import get_deepseek_response
from backend.comparator import compare_answers

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev/demo; restrict in production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Multi-Model Chatbot API is running"}

@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    image_base64 = None
    image_bytes = None
    mime_type = None

    if image:
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        mime_type = image.content_type

    # Run all model requests concurrently
    tasks = [
        get_chatgpt_response(question, image_base64),
        get_gemini_response(question, image_bytes, mime_type),
        get_deepseek_response(question)
    ]

    results = await asyncio.gather(*tasks)

    chatgpt_res = results[0]
    gemini_res = results[1]
    deepseek_res = results[2]

    answers = {
        "ChatGPT": chatgpt_res,
        "Gemini": gemini_res,
        "DeepSeek": deepseek_res
    }

    # Compare answers
    comparison_result = await compare_answers(question, answers)
    
    # Determine best answer text
    best_model = comparison_result.get("best_model", "")
    best_answer_text = answers.get(best_model, "")

    return {
        "best_answer": {
            "model": best_model,
            "text": best_answer_text,
            "reason": comparison_result.get("reason", "")
        },
        "all_answers": answers
    }
