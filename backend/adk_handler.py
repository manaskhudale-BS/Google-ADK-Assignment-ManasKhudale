import os
import tempfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import google.generativeai as genai
from google.cloud import speech
from langchain_community.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load Chroma database
db = Chroma(persist_directory="./vector_db", embedding_function=embeddings)

# Initialize Google Cloud Speech client
client = speech.SpeechClient()


# --- Function: Transcribe audio to text ---
def transcribe_audio(audio_path):
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return "Could not transcribe audio."
    return response.results[0].alternatives[0].transcript


# --- Function: Query the vector DB and LLM ---
def query_hr_handbook(query_text):
    docs = db.similarity_search(query_text, k=2)
    if not docs:
        return "No relevant section found in the handbook.", ""

    context = "\n\n".join([doc.page_content for doc in docs])
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    prompt = f"""
You are an HR assistant. Answer the question below based only on the given handbook text.

Question: {query_text}

Handbook Context:
{context}
"""
    response = model.generate_content(prompt)
    return response.text.strip(), context


# --- Function: Convert AI text response to speech ---
def text_to_speech(text, filename):
    tts = gTTS(text)
    tts.save(filename)


# --- Function: Generate a concise summary of the chat ---
def generate_summary(query, response_text):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        prompt = f"Summarize the following HR assistant conversation in 2-3 sentences:\n\nUser: {query}\nAI: {response_text}"
        summary = model.generate_content(prompt)
        return summary.text.strip()
    except Exception:
        return "No summary available."


# --- Function: Send transcript email to the user ---
def send_summary_email(to_email, user_name, query_text, response_text, referenced_text):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Generate a summary using Gemini
    summary = generate_summary(query_text, response_text)

    subject = "Your HR Assistant Chat Summary"
    body = f"""
Hi {user_name},

Here’s a summary of your recent interaction with the HR Assistant.

Your Question:
{query_text}

AI’s Response:
{response_text}

Summary:
{summary}

Referenced Handbook Sections:
{referenced_text if referenced_text else "No specific sections referenced."}

Thank you for using the BigStep HR Assistant.
"""

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")


# --- Function: Full pipeline handler ---
def process_audio_query(audio_path, name, email):
    # Step 1: Transcribe user’s question
    query_text = transcribe_audio(audio_path)
    print(f"[User Query]: {query_text}")

    # Step 2: Retrieve handbook info + AI response
    response_text, retrieved_text = query_hr_handbook(query_text)
    print(f"[Retrieved Handbook Text]: {retrieved_text[:150]}...")
    print(f"[AI Response]: {response_text}")

    # Step 3: Convert AI response to speech
    text_to_speech(response_text, "response.mp3")

    # Step 4: Send summary email
    # send_summary_email(email, name, query_text, response_text, retrieved_text)

    # Step 5: Return path of generated audio
    return "response.mp3"
