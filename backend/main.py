from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import tempfile
from fastapi.middleware.cors import CORSMiddleware
import os
from adk_handler import process_audio_query

# Load environment variables
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5501"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Backend running successfully"}

@app.post("/api/query")
async def query(audio: UploadFile, name: str = Form(...), email: str = Form(...)):
    # Save the incoming audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    # Pass it through Google ADK workflow
    output_audio = process_audio_query(tmp_path, name, email)

    # Return generated voice response
    return FileResponse(output_audio, media_type="audio/mp3", filename="response.mp3")
