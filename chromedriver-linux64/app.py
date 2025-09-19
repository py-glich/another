import os, time, streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CHROME_BIN = "/usr/bin/chromium"
CHROMEDRIVER = "/usr/bin/chromedriver"
os.chmod(CHROMEDRIVER, 0o755)

options = Options()
options.binary_location = CHROME_BIN
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--mute-audio")

service = Service(CHROMEDRIVER)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://meet.google.com/your-meet-code")
time.sleep(8)
st.write("title:", driver.title)
driver.quit()




