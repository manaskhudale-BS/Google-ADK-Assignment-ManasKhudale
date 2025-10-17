# Google-ADK-Assignment-ManasKhudale


https://github.com/user-attachments/assets/8ae91097-b6ad-43d5-bef2-896ee7eaf251


## Voice-Based HR Assistant

This project is an AI-powered **voice-enabled HR assistant** that allows employees to ask company-related questions verbally and receive AI-generated voice responses based on the **Employee Handbook**.

It integrates **FastAPI**, **ChromaDB**, and **Google’s Gemini 2.5 Flash model** to perform end-to-end speech understanding, context retrieval, and response generation.

---

## Features
- Voice input for natural interaction  
- Handbook-based intelligent answers using ChromaDB  
- Voice output generated from Gemini 2.5 Flash  
- Simple and responsive web interface (HTML, CSS, JS)  
- Fully local execution with minimal setup  

---

## Tech Stack
| Component | Technology Used |
|------------|----------------|
| Frontend | HTML, CSS, JavaScript |
| Backend Framework | FastAPI |
| Database / Vector Store | ChromaDB |
| Embedding Generator | LangChain + Gemini Embeddings |
| AI Model | Gemini 2.5 Flash |
| Transcription & Text-to-Speech | Gemini 2.5 Flash |
| Handbook Parsing | LangChain DocumentLoader + RecursiveCharacterTextSplitter |

---

## Project Flow
1. The user enters their name and email once.  
2. The user speaks a question using the microphone.  
3. The audio is sent to the backend for transcription using Gemini.  
4. The text query is matched with the embedded Employee Handbook using ChromaDB.  
5. Gemini 2.5 Flash generates a contextual answer.  
6. The AI response is converted to speech and returned to the frontend for playback.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/manaskhudale-BS/Google-ADK-Assignment-ManasKhudale.git
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file inside the `backend` directory:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Parse the Employee Handbook

Place your handbook file (PDF or TXT) in the `backend` directory, then run:

```bash
python3 parse_handbook.py
```

### 5. Start the Backend Server

```bash
cd backend
python3 -m uvicorn main:app --reload
```

### 6. Run the Frontend

In another terminal:

```bash
cd frontend
python3 -m http.server 5501
```

Then open [http://localhost:5501](http://localhost:5501) in your browser.

---

## Example Interaction

**User:** What is the dress code?
**AI:** Our dress code is business casual unless specified otherwise for client meetings or events.

**User:** What is the policy on conflicts of interest?
**AI:** Employees must avoid situations where personal interests conflict with company interests and disclose any potential conflicts to HR.

---

## Project Structure

```
Voice-HR-Assistant
├── backend/
│   ├── main.py              # FastAPI server
│   ├── adk_handler.py       # Handles transcription, AI logic, and TTS
│   ├── db.py                # ChromaDB setup and retrieval
│   ├── parse_handbook.py    # Splits and embeds handbook text
│   ├── .env                 # Gemini API key
│   └── vector_db/           # Embedded vector data
│
├── frontend/
│   ├── index.html           # Main user interface
│   ├── style.css            # Page styling
│   ├── script.js            # Handles mic recording and playback
│
└── README.md
```

## Author

**Manas Khudale**


