// Set this to your deployed backend URL.
// For local testing, use http://localhost:8000
const API_URL = "http://localhost:8000";
// IMPORTANT: AFTER deploying backend to Render, replace the line above with your Render URL
// Example: const API_URL = "https://my-chatbot.onrender.com"; 

const questionInput = document.getElementById('questionInput');
const imageInput = document.getElementById('imageInput');
const submitBtn = document.getElementById('submitBtn');
const fileNameDisplay = document.getElementById('fileName');
const loadingDiv = document.getElementById('loading');
const resultsArea = document.getElementById('resultsArea');

// File input handler
imageInput.addEventListener('change', () => {
    if (imageInput.files.length > 0) {
        fileNameDisplay.textContent = imageInput.files[0].name;
    } else {
        fileNameDisplay.textContent = '';
    }
});

// Submit handler
submitBtn.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    const imageFile = imageInput.files[0];

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    // UI State: Loading
    submitBtn.disabled = true;
    loadingDiv.classList.remove('hidden');
    resultsArea.classList.add('hidden');

    const formData = new FormData();
    formData.append('question', question);
    if (imageFile) {
        formData.append('image', imageFile);
    }

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);

    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong silently. Please check console.");
    } finally {
        submitBtn.disabled = false;
        loadingDiv.classList.add('hidden');
    }
});

function renderResults(data) {
    resultsArea.classList.remove('hidden');

    // Best Answer
    const best = data.best_answer;
    document.getElementById('bestModelName').textContent = best.model;
    document.getElementById('bestAnswerContent').innerHTML = marked.parse(best.text || "No text returned.");
    document.getElementById('winReason').textContent = best.reason;

    // Others
    const all = data.all_answers;

    // Update individual cards
    document.getElementById('chatgptContent').innerHTML = marked.parse(all.ChatGPT || "No response");
    document.getElementById('geminiContent').innerHTML = marked.parse(all.Gemini || "No response");
    document.getElementById('deepseekContent').innerHTML = marked.parse(all.DeepSeek || "No response");
}
