import io
import os
from google.cloud import speech, texttospeech
import google.generativeai as genai
from db import search_handbook
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def process_audio_query(audio_path, name, email):
    """Main logic to handle user voice input, ADK processing, and voice output"""
    # Convert user audio to text
    query_text = transcribe_audio(audio_path)
    print(f"[User Query]: {query_text}")

    # Search Employee Handbook using embeddings
    handbook_answer = search_handbook(query_text)
    print(f"[Retrieved Handbook Text]: {handbook_answer[:150]}...")

    # Use Google Gemini model to generate a summarized, natural response
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")  
    prompt = f"""
    You are an HR voice assistant for BigStep company.
    The user asked: {query_text}
    Using this handbook info: {handbook_answer}
    Provide a short, clear, professional spoken response.
    """
    response = model.generate_content(prompt)
    final_text = response.text.strip()
    print(f"[AI Response]: {final_text}")

    # Convert AI response to speech
    output_path = "response.mp3"
    synthesize_speech(final_text, output_path)

    return output_path


def transcribe_audio(file_path):
    """Speech-to-text using Google Cloud Speech API"""
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return "Could not transcribe audio."
    return response.results[0].alternatives[0].transcript


def synthesize_speech(text, output_file):
    """Text-to-speech using Google Cloud TTS API"""
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f"[Voice Response Saved]: {output_file}")
