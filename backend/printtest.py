import google.generativeai as genai
genai.configure(api_key="AIzaSyAlliWwwfZM_kdzMvFz3AE1UtfedcFywN4")
model = genai.GenerativeModel("models/gemini-2.5-flash")
resp = model.generate_content("Summarize: why leave policy matters")
print(resp.text)
