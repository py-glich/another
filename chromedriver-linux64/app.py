import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import openai
from threading import Thread

# ------------------------------
# 🔹 Streamlit UI
# ------------------------------
st.set_page_config(page_title="Google Meet Assistant", layout="wide")
st.title("🌌 Google Meet Assistant")

meet_code = st.text_input("Enter your Google Meet code (e.g., txe-ditf-qgs):")

if "subtitles" not in st.session_state:
    st.session_state.subtitles = []
if "responses" not in st.session_state:
    st.session_state.responses = []

# ------------------------------
# 🔹 OpenAI Setup
# ------------------------------
openai.api_key = "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"

def ask_ai(question):
    try:
        response = openai.chat.completions.create(
            model="google/gemini-2.0-flash-lite-001",
            messages=[{"role": "user", "content": question}]
        )
        if response and hasattr(response, 'choices') and response.choices:
            return response.choices[0].message.content.strip()
        return "⚠ No valid response from AI"
    except Exception as e:
        return f"🚨 API Error: {str(e)}"

# ------------------------------
# 🔹 ChromeDriver Setup
# ------------------------------
def start_driver():
    DRIVER_PATH = os.path.join(os.path.dirname(__file__), "chromedriver")

    options = Options()
    # ⚠️ Start with GUI so you can log in manually first
    # comment this when you confirm it works
    # options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# ------------------------------
# 🔹 Meeting Bot
# ------------------------------
def run_meeting_bot(meet_code):
    try:
        driver = start_driver()
        driver.get("https://meet.google.com/")
        time.sleep(5)

        meeting_link = f"https://meet.google.com/{meet_code}"
        driver.get(meeting_link)
        time.sleep(10)

        st.session_state.subtitles.append("✅ Google Meet page opened. Please ensure you are logged in!")

        while True:
            # Debug: print all text nodes
            all_divs = driver.find_elements(By.TAG_NAME, "div")
            for d in all_divs[-10:]:  # check last 10 divs
                txt = d.text.strip()
                if txt:
                    st.session_state.subtitles.append(f"[DEBUG] {txt}")
                    break

            subtitles = driver.find_elements(By.CLASS_NAME, "iOzk7")
            if subtitles:
                last_subtitle = subtitles[-1].text.strip()
                if last_subtitle and (not st.session_state.subtitles or st.session_state.subtitles[-1] != last_subtitle):
                    st.session_state.subtitles.append(last_subtitle)
                    answer = ask_ai(last_subtitle)
                    st.session_state.responses.append(answer)
            time.sleep(2)

    except Exception as e:
        st.session_state.subtitles.append(f"🛑 Error: {e}")

# ------------------------------
# 🔹 Start Button
# ------------------------------
if st.button("🚀 Join Meeting"):
    if meet_code:
        thread = Thread(target=run_meeting_bot, args=(meet_code,))
        thread.daemon = True
        thread.start()
        st.success("Joining meeting... extracting subtitles...")
    else:
        st.error("Meeting code is required!")

#

