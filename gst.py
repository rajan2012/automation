from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import getpass

# Function to automate GST login
def gst_login():
    # Get password securely from the console
    # password = getpass.getpass("Enter your GST portal password: ")

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH

    try:
        # Open GST login page
        driver.get("https://services.gst.gov.in/services/login")
        driver.maximize_window()
        time.sleep(3)  # Allow the page to load

        # Input username using name attribute
        username_field = driver.find_element(By.NAME, "Username")
        username_field.send_keys("sah_gst123")

        # Input password using name attribute
        password_field = driver.find_element(By.NAME, "Password")
        password_field.send_keys("Kama@1234")

        # Click on the login button using name attribute
        login_button = driver.find_element(By.NAME, "gst_signin")
        login_button.click()

        # Wait for the login process to complete
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

# Run the function
gst_login()
