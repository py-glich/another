import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

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
    # ✅ Automatically install correct ChromeDriver
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
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



