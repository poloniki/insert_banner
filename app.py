from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time
import base64
import streamlit as st


# Function to inject a horizontal top banner into a given URL and take a screenshot with predefined resolution
def inject_banner(url, banner_path, output_file, width, height):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for testing
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # Larger window size

    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=chrome_options,
        )

        # Set the window size to the predefined resolution
        driver.set_window_size(width, height)

        # Open the given URL
        driver.get(url)
        time.sleep(5)  # Increased wait time for the page to load

        # Read the local image file and encode it as a base64 string
        with open(banner_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        # Create a base64 data URL
        banner_url = f"data:image/png;base64,{encoded_string}"

        # Inject a horizontal top banner by manipulating the DOM
        script = f"""
        var banner = document.createElement("img");
        banner.src = "{banner_url}";
        banner.style.position = "fixed";
        banner.style.top = "0";
        banner.style.left = "0";
        banner.style.width = "100%";
        banner.style.height = "100px";
        document.body.appendChild(banner);
        """
        driver.execute_script(script)
        time.sleep(5)  # Wait for the script to execute

        # Take a screenshot with the predefined resolution
        driver.save_screenshot(output_file)
        print(f"Screenshot saved as {output_file}")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        if driver:
            driver.quit()


banner_path = "banners/image.png"
output_file = "injected_banner_screenshot.png"
width = 728
height = 1080

with st.form("url"):
    url = st.text_input("URL")
    button = st.form_submit_button("Insert MMA banner")

if button:
    injected = inject_banner(url, banner_path, output_file, width, height)
    if injected:
        st.image(output_file, caption="MMA Banner Screenshot")
