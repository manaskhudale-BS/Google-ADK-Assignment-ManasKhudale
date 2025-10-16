# list_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")   # adjust path if your .env is elsewhere
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    models = genai.list_models()
    print("Available models (name, description):\n")
    for m in models:
        name = getattr(m, "name", str(m))
        desc = getattr(m, "display_name", "") or getattr(m, "description", "")
        print(f"- {name}    {(' - ' + desc) if desc else ''}")
except Exception as e:
    print("ERROR listing models:", repr(e))
