import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

async def compare_answers(question, answers):
    """
    Compares answers from different models and selects the best one.
    answers: dict { "ChatGPT": "...", "Gemini": "...", "DeepSeek": "..." }
    """
    if not GEMINI_API_KEY:
        # Fallback if no API key for judge
        return {
            "best_model": "Unknown (No Judge Key)",
            "reason": "Comparator could not run due to missing API key.",
            "best_answer": "N/A"
        }

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an intelligent judge.
        
        Question: {question}
        
        Answers:
        1. ChatGPT: {answers.get('ChatGPT', 'No response')}
        2. Gemini: {answers.get('Gemini', 'No response')}
        3. DeepSeek: {answers.get('DeepSeek', 'No response')}
        
        Task:
        Evaluate these answers based on accuracy, clarity, and completeness.
        Select the best answer.
        
        Return your response in strictly VALID JSON format request with these keys:
        - "best_model": "ChatGPT" or "Gemini" or "DeepSeek"
        - "reason": "A brief explanation of why this is the best answer."
        """
        
        response = model.generate_content(prompt)
        
        # simple cleanup for markdown code blocks if present
        text = response.text
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        result = json.loads(text.strip())
        return result

    except Exception as e:
        return {
            "best_model": "Error",
            "reason": f"Comparator failed: {str(e)}",
            "best_answer": "Error"
        }
