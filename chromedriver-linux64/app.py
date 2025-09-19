import streamlit as st
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import openai

# =========================
# CONFIG
# =========================
OPENAI_API_KEY = "your_api_key_here"
openai.api_key = OPENAI_API_KEY

# Path to chromedriver (already downloaded and placed in project folder)
DRIVER_PATH = os.path.join(os.path.dirname(__file__), "chromedriver")

# Path to your Chrome profile (adjust to your system)
# On Linux:
PROFILE_PATH = "/home/yourusername/.config/google-chrome"
# On Windows (example):
# PROFILE_PATH = r"C:\Users\YourName\AppData\Local\Google\Chrome\User Data"

# =========================
# FUNCTIONS
# =========================
def start_driver():
    options = Options()
    options.add_argument(f"--user-data-dir={PROFILE_PATH}")
    options.add_argument("--profile-directory=Default")  # change if you use another profile
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def join_meeting(meet_code):
    meeting_link = f"https://meet.google.com/{meet_code}"
    driver = start_driver()

    try:
        driver.get(meeting_link)
        time.sleep(10)  # wait for page to load

        # Try clicking "Join now"
        try:
            join_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Join now')]/..")
            join_btn.click()
            st.success("✅ Joined the meeting successfully!")
        except Exception:
            st.warning("⚠ Could not find 'Join now' button, maybe already in meeting?")

        return driver
    except Exception as e:
        st.error(f"❌ Failed to open meeting: {e}")
        return None

def extract_subtitles(driver):
    try:
        captions = driver.find_elements(By.CSS_SELECTOR, "div[jsname='YS01Ge']")
        texts = [c.text for c in captions if c.text.strip()]
        return texts[-1] if texts else ""
    except Exception:
        return ""

def ask_chatgpt(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"⚠ ChatGPT error: {e}"

# =========================
# STREAMLIT APP
# =========================
st.title("Google Meet Assistant 🤖")

if "driver" not in st.session_state:
    st.session_state.driver = None

meet_code = st.text_input("Enter your Google Meet code (e.g., abc-defg-hij)")

if st.button("Join Meeting"):
    if meet_code:
        st.session_state.driver = join_meeting(meet_code)
    else:
        st.error("❌ Please enter a meeting code!")

if st.button("Start Listening"):
    if st.session_state.driver:
        st.info("🎤 Listening to subtitles...")
        placeholder = st.empty()
        while True:
            text = extract_subtitles(st.session_state.driver)
            if text:
                placeholder.text(f"📝 Subtitle: {text}")
                answer = ask_chatgpt(text)
                st.write(f"🤖 ChatGPT: {answer}")
            time.sleep(5)
    else:
        st.error("❌ You must join a meeting first!")




