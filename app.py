from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time
import base64
import streamlit as st


@st.cache_resource
def get_driver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for testing
    chrome_options.add_argument("--disable-gpu")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=chrome_options,
    )


# Function to inject a horizontal top banner into a given URL and take a screenshot with predefined resolution
def inject_banner(url, banner_path, output_file, width, height):
    # Ensure you have ChromeDriver installed
    driver = get_driver()
    try:
        # Set the window size to the predefined resolution
        driver.set_window_size(width, height)

        # Open the given URL
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

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
        banner.style.height = "100px";  // Adjust the height of the banner as needed
        document.body.appendChild(banner);
        """
        driver.execute_script(script)
        time.sleep(1)  # Wait for the script to execute

        # Take a screenshot with the predefined resolution
        driver.save_screenshot(output_file)
        print(f"Screenshot saved as {output_file}")
        return True

    finally:
        driver.quit()


banner_path = "banners/image.png"
output_file = "injected_banner_screenshot.png"
width = 728
height = 1080


with st.form("url"):
    url = st.text_input("Url")
    button = st.form_submit_button("Insert MMA banner")

if button:
    injected = inject_banner(url, banner_path, output_file, width, height)
    if injected:
        st.image("injected_banner_screenshot.png", caption="MMA")
