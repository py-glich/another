from flask import Flask, render_template, request, jsonify
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading, time

app = Flask(__name__)

# ----------------------------
# OpenAI / OpenRouter API Setup
# ----------------------------
client = openai.OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def ask_ai(question):
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-001",
            messages=[{"role": "user", "content": question}]
        )
        if response and hasattr(response, 'choices') and response.choices:
            return response.choices[0].message.content.strip()
        return "⚠ No valid response from AI"
    except Exception as e:
        return f"🚨 API Error: {str(e)}"

# ----------------------------
# Selenium Meet Bot
# ----------------------------
captured_subtitles = []
captured_responses = []

def run_meeting_bot(meet_code):
    try:
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--mute-audio")
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(f"https://meet.google.com/{meet_code}")
        time.sleep(10)

        while True:
            subtitles = driver.find_elements(By.CLASS_NAME, "iOzk7")
            if subtitles:
                last_subtitle = subtitles[-1].text.strip()
                if last_subtitle not in captured_subtitles:
                    captured_subtitles.append(last_subtitle)
                    answer = ask_ai(last_subtitle)
                    captured_responses.append(answer)
            time.sleep(2)

    except Exception as e:
        print("Bot Error:", e)

# ----------------------------
# Flask Routes
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")  # frontend UI

@app.route("/subtitles")
def get_subtitles():
    return jsonify(captured_subtitles)

@app.route("/responses")
def get_responses():
    return jsonify(captured_responses)

@app.route("/start/<meet_code>")
def start_bot(meet_code):
    thread = threading.Thread(target=run_meeting_bot, args=(meet_code,))
    thread.daemon = True
    thread.start()
    return f"✅ Bot started for Meet code {meet_code}"

# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)









