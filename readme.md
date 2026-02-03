# Multi-Model AI Chatbot

A full-stack web application that allows users to ask questions (Text & Image) and get answers from **ChatGPT (GPT-4o)**, **Gemini 1.5 Flash**, and **DeepSeek**. The system also includes an AI Judge that automatically selects the best answer.

## Project Structure

```
/backend
    /main.py        # FastAPI application & endpoints
    /chatgpt.py     # OpenAI API client
    /gemini.py      # Google Gemini API client
    /deepseek.py    # DeepSeek API client (OpenAI compatible)
    /comparator.py  # Logic to compare answers using an LLM Judge
    /.env           # Environment variables (API Keys)
/frontend
    /index.html     # Main user interface
    /style.css      # Styling (Dark mode, specialized UI)
    /script.js      # Frontend logic & API calls
requirements.txt    # Python dependencies
Procfile            # Deployment command for Render
netlify.toml        # Deployment config for Netlify
```

## Setup Instructions

### 1. Backend Setup

1.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Keys**:
    - Open `backend/.env`.
    - Retrieve API keys for:
        - **OpenAI** (for ChatGPT)
        - **Google Gemini**
        - **DeepSeek**
    - Paste them into the `.env` file.

3.  **Run Locally**:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will run at `http://127.0.0.1:8000`.

### 2. Frontend Setup

1.  Navigate to the `frontend/` folder.
2.  Open `index.html` in your browser.
    - *Tip: Use "Live Server" extension in VS Code for best experience.*
3.  **Important**: By default, `script.js` points to `http://localhost:8000`.

---

## Deployment Guide

### Backend (Render.com)
1.  Push this repository to GitHub/GitLab.
2.  Create a new **Web Service** on Render.
3.  Connect your repository.
4.  **Settings**:
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` (or use the provided `Procfile`)
    - **Root Directory**: `.` (default)
5.  **Environment Variables**:
    - Add `OPENAI_API_KEY`, `GEMINI_API_KEY`, `DEEPSEEK_API_KEY` in the Render dashboard.
6.  **Copy the URL**: Once deployed, copy your backend URL (e.g., `https://my-chatbot.onrender.com`).

### Frontend (Netlify)
1.  **Update API URL**:
    - Open `frontend/script.js`.
    - Change `const API_URL = "http://localhost:8000";` to your Render URL:
        ```javascript
        const API_URL = "https://my-chatbot.onrender.com";
        ```
2.  **Deploy**:
    - Drag and drop the `frontend` folder to Netlify Drop, OR
    - Connect your GitHub repo to Netlify.
    - **Build Settings**:
        - **Base directory**: `frontend` (or leave empty if root)
        - **Publish directory**: `frontend`
3.  The site is now live!

## Features
- **Multi-Model Intelligence**: Queries 3 top LLMs simultaneously.
- **Vision Support**: Upload images for analysis by GPT-4o and Gemini.
- **Auto-Evaluation**: An AI Judge evaluates responses and highlights the winner.
- **Response Comparison**: View all raw responses side-by-side.
