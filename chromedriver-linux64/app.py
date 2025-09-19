import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Google Meet Assistant", layout="wide")
st.title("🌌 Google Meet Assistant")

meet_code = st.text_input("Enter Google Meet code (e.g. txe-ditf-qgs):")
join_button = st.button("🚀 Join Meeting")

# -----------------------------
# Selenium Driver Setup
# -----------------------------
def start_driver():
    # ✅ Path to chromedriver in same folder as app.py
    DRIVER_PATH = os.path.join(os.path.dirname(__file__), "chromedriver")

    # ✅ Fix permission for Streamlit Cloud
    os.chmod(DRIVER_PATH, 0o755)

    options = webdriver.ChromeOptions()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# -----------------------------
# Join Meeting
# -----------------------------
def join_meeting(meet_code):
    driver = start_driver()
    meeting_link = f"https://meet.google.com/{meet_code}"

    st.info("🔄 Opening Google Meet...")
    driver.get(meeting_link)
    time.sleep(10)

    try:
        # Try clicking "Join now"
        join_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Join now')]/..")
        join_btn.click()
        st.success("✅ Successfully joined the meeting!")
    except Exception as e:
        st.error(f"⚠ Could not click Join now: {e}")

    return driver

# -----------------------------
# Handle Join Button
# -----------------------------
if join_button and meet_code:
    try:
        driver = join_meeting(meet_code)
        st.session_state.driver = driver
    except Exception as e:
        st.error(f"❌ Failed to open meeting: {e}")



