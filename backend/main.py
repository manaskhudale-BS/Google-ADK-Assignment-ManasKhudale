from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from adk_handler import process_audio_query, send_summary_email
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------
# 🎤 API endpoint: handle audio query from frontend
# -----------------------------------------------
@app.post("/api/query")
async def query(audio: UploadFile = File(...), name: str = Form(...), email: str = Form(...)):
    """Handle user voice query, process with Gemini + HR handbook."""
    try:
        # Save uploaded audio temporarily
        temp_path = f"temp_{audio.filename}"
        with open(temp_path, "wb") as f:
            f.write(await audio.read())

        # Process query using ADK handler logic
        output_audio = process_audio_query(temp_path, name, email)

        # Return the AI’s audio response to frontend
        return FileResponse(output_audio, media_type="audio/mp3", filename="response.mp3")

    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to process query", "details": str(e)},
        )

# -----------------------------------------------
# 📩 API endpoint: send summary email after chat ends
# -----------------------------------------------
@app.post("/api/end_chat")
async def end_chat(name: str = Form(...), email: str = Form(...)):
    """Send chat summary email when the user ends the conversation."""
    try:
        # Example summary (you can dynamically generate this later)
        query_text = "User asked about HR policies including dress code and conflict of interest."
        response_text = "The assistant provided HR policy details from the handbook."
        referenced_text = "Referenced sections: Dress Code, Conflict of Interest, Code of Conduct."

        # Send email via SMTP
        send_summary_email(email, name, query_text, response_text, referenced_text)

        print(f"✅ Summary email sent to {email}")
        return {"status": "success", "message": "Email sent successfully"}

    except Exception as e:
        print(f"❌ Failed to send summary email: {e}")
        return {"status": "error", "message": str(e)}

# -----------------------------------------------
# ✅ Root endpoint (optional)
# -----------------------------------------------
@app.get("/")
def home():
    return {"message": "HR Voice Assistant Backend is running!"}
