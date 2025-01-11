
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time

def select_financial_year_and_quarter(driver):
    try:
        # Select Financial Year
        fin_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "fin"))
        )
        select_fin = Select(fin_dropdown)
        select_fin.select_by_index(1)
        selected_fin = select_fin.first_selected_option.text
        print(f"Successfully selected financial year: {selected_fin}")

        # Wait for page to update
        time.sleep(6)

        # Select Quarter with retry mechanism
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                quarter_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "quarter"))
                )
                select_quarter = Select(quarter_dropdown)
                select_quarter.select_by_index(1)
                selected_quarter = select_quarter.first_selected_option.text
                print(f"Successfully selected quarter: {selected_quarter}")
                break
            except StaleElementReferenceException:
                if attempt < max_attempts - 1:
                    print("Stale element, retrying...")
                    time.sleep(2)
                else:
                    raise
        max_attempts = 3
        # Select Period with retry mechanism
        for attempt in range(max_attempts):
            try:
                period_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "mon"))
                )
                select_period = Select(period_dropdown)
                select_period.select_by_index(1)
                selected_period = select_period.first_selected_option.text
                print(f"Successfully selected period: {selected_period}")
                break
            except StaleElementReferenceException:
                if attempt < max_attempts - 1:
                    print("Stale element, retrying...")
                    time.sleep(2)
                else:
                    raise

    except Exception as e:
        print(f"An error occurred: {e}")

def select_financial_year_quarter_and_period(driver):
    try:
        # Select Financial Year
        fin_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "fin"))
        )
        select_fin = Select(fin_dropdown)
        select_fin.select_by_index(1)
        selected_fin = select_fin.first_selected_option.text
        print(f"Successfully selected financial year: {selected_fin}")

        # Wait for page to update
        time.sleep(6)

        # Select Quarter with retry mechanism
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                quarter_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "quarter"))
                )
                select_quarter = Select(quarter_dropdown)
                select_quarter.select_by_index(1)
                selected_quarter = select_quarter.first_selected_option.text
                print(f"Successfully selected quarter: {selected_quarter}")
                break
            except StaleElementReferenceException:
                if attempt < max_attempts - 1:
                    print("Stale element, retrying...")
                    time.sleep(2)
                else:
                    raise

        # Wait for page to update after quarter selection
        time.sleep(6)

        # Select Period with retry mechanism
        for attempt in range(max_attempts):
            try:
                period_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "mon"))
                )
                select_period = Select(period_dropdown)
                select_period.select_by_index(1)
                selected_period = select_period.first_selected_option.text
                print(f"Successfully selected period: {selected_period}")
                break
            except StaleElementReferenceException:
                if attempt < max_attempts - 1:
                    print("Stale element, retrying...")
                    time.sleep(2)
                else:
                    raise

    except Exception as e:
        print(f"An error occurred: {e}")

def gst_login():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://services.gst.gov.in/services/login")
        driver.maximize_window()
        time.sleep(3)

        driver.find_element(By.NAME, "user_name").send_keys("sah_gst123")
        driver.find_element(By.ID, "user_pass").send_keys("Kama@1234")

        print("Please enter the captcha manually.")
        time.sleep(20)

        login_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()

        WebDriverWait(driver, 30).until(EC.url_changes(driver.current_url))
        print("Login successful!")

        time.sleep(7)

        dashboard_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Return Dashboard"]'))
        )

        # Scroll into view if necessary and click on it
        ActionChains(driver).move_to_element(dashboard_link).perform()
        dashboard_link.click()

        # Verify that the navigation was successful
        print("New page title:", driver.title)
        print("New page URL:", driver.current_url)

        #select_financial_year_quarter_and_period(driver)
        select_financial_year_and_quarter(driver)




    except Exception as e:
        print(f"An error occurred: {e}")

    print("Browser will remain open. Close it manually when done.")


# Assuming you have already logged in and navigated to the correct page
# Call this function after successful login


gst_login()
