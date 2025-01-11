

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path
import os

# Example: Creating a WebDriver instance with an extended timeout
options = webdriver.ChromeOptions()

# Optional: Add more options if needed
options.add_argument("--start-maximized")

# Adjust desired capabilities
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal"  # Ensures full page load before timeout

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


def wait_for_dropdown(driver, dropdown_name, retries=3):
    """
    Wait for a dropdown to load completely.
    """
    for attempt in range(retries):
        try:
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, dropdown_name))
            )
            select = Select(dropdown)
            if len(select.options) > 1:  # Ensure dropdown has options loaded
                return select
            else:
                print(f"Retrying {dropdown_name}... Options not loaded (attempt {attempt + 1})")
                time.sleep(3)
        except Exception as e:
            print(f"Error loading {dropdown_name}: {e}")
            time.sleep(3)
    raise Exception(f"Dropdown {dropdown_name} did not load after {retries} retries")


def select_options_and_search(driver,index):
    try:
        #go through all for quarter
        #for just first qurarter -0,1 and likewise
        for q_index in range(3,4):  # Iterate over quarters
            time.sleep(2)

            # Select Financial Year
            select_fin = wait_for_dropdown(driver, "fin")
            #0 -current year
            # 1 -previous year
            # 1 -2 year back
            # 1 -3 year back
            select_fin.select_by_index(index)
            selected_fin = select_fin.first_selected_option.text
            #print(f"Successfully selected financial year: {selected_fin}")
            time.sleep(3)

            # Select Quarter
            select_quarter = wait_for_dropdown(driver, "quarter")
            select_quarter.select_by_index(q_index)
            selected_quarter = select_quarter.first_selected_option.text
            #print(f"Selected quarter: {selected_quarter}")
            time.sleep(3)

            # Select Period
            select_period = wait_for_dropdown(driver, "mon")
            #3 means
            #go through all months in each quater
            #to select one specific month
            #replace by(0,1)-for 1st month
            #1,2 -for second and likewise
            for p_index in range(2,3):  # Iterate over periods
                time.sleep(5)
                select_period.select_by_index(p_index)
                selected_period = select_period.first_selected_option.text
                #print(f"Selected period: {selected_period}")
                time.sleep(3)

                # Click Search Button
                search_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.srchbtn[type='submit']"))
                )
                search_button.click()
                print("Clicked Search button")

                # Handle View Button
                view_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary smallbutton' and contains(@data-ng-click, 'page_rtp')]"))
                )
                driver.execute_script("arguments[0].click();", view_button)
                print("Clicked VIEW button")

                try:
                    # Handle DOWNLOAD FILED (PDF) Button
                    download_button = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary' and contains(@data-ng-click, 'generateNILGstr1Pdf')]"))
                    )
                    driver.execute_script("arguments[0].click();", download_button)
                    #print("Clicked DOWNLOAD FILED (PDF) button")
                    print(f"Download 2b view for 2023-2024, {selected_quarter}, {selected_period}")
                    time.sleep(4)
                    driver.back()
                    time.sleep(3)
                    driver.refresh()

                    WebDriverWait(driver, 10).until(EC.staleness_of(download_button))  # Wait for page reload
                    print("Navigated back to the previous page")
                except Exception as e:
                    print(f"DOWNLOAD FILED (PDF) button not found: {e}")

                    # Handle VIEW SUMMARY workflow
                    try:
                        view_summary_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'VIEW SUMMARY')]"))
                        )
                        driver.execute_script("arguments[0].click();", view_summary_button)
                        print("Clicked VIEW SUMMARY button")
                        time.sleep(5)

                        download_pdf_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'DOWNLOAD (PDF)')]"))
                        )
                        driver.execute_script("arguments[0].click();", download_pdf_button)
                        print("Clicked DOWNLOAD (PDF) button")
                        time.sleep(4)
                        print(f"Download 2b view summary for 2023-2024, {selected_quarter}, {selected_period}")
                        driver.back()
                        time.sleep(4)
                        WebDriverWait(driver, 10).until(EC.staleness_of(download_pdf_button))  # Wait for page reload
                        print("Navigated back to the previous page")
                        driver.back()
                        time.sleep(3)
                        driver.refresh()
                        time.sleep(10)
                        WebDriverWait(driver, 10).until(EC.staleness_of(view_summary_button))  # Wait for page reload
                        print("Navigated back to the previous page")
                    except Exception as inner_exception:
                        print(f"Error in VIEW SUMMARY workflow: {inner_exception}")

                time.sleep(5)

                # Ensure elements are reloaded
                print("resetetting again")
                select_fin = wait_for_dropdown(driver, "fin")
                select_fin.select_by_index(1)
                #print("Financial year reset")
                time.sleep(2)

                select_quarter = wait_for_dropdown(driver, "quarter")
                select_quarter.select_by_index(q_index)
                #print("Quarter reset")

                select_period = wait_for_dropdown(driver, "mon")
                select_period.select_by_index(p_index)
                #print("Period reset")
                time.sleep(2)

                # Click Search Button after reset
                search_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.srchbtn[type='submit']"))
                )
                search_button.click()
                print("Clicked Search button after reset")

                # Find and click the Download button
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@class='btn btn-primary pull-right' and @data-ng-click='downloadGSTR3Bpdf()']")
                    )
                )
                driver.execute_script("arguments[0].click();", download_button)
                #print("Clicked Download button")
                print(f"Download 3b for {selected_fin}, {selected_quarter}, {selected_period}")
                time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")



def gst_login(username, password, index, driver):
    try:
        driver.get("https://services.gst.gov.in/services/login")
        driver.maximize_window()
        time.sleep(3)

        # Enter credentials
        driver.find_element(By.NAME, "user_name").send_keys(username)
        driver.find_element(By.ID, "user_pass").send_keys(password)

        print("Please enter the captcha manually.")
        time.sleep(20)

        # Click the login button
        login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()

        WebDriverWait(driver, 30).until(EC.url_changes(driver.current_url))
        print("Login successful!")

        time.sleep(7)

        # Navigate to the dashboard
        dashboard_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Return Dashboard"]'))
        )
        ActionChains(driver).move_to_element(dashboard_link).perform()
        dashboard_link.click()

        print("New page title:", driver.title)
        print("New page URL:", driver.current_url)

        time.sleep(3)

        # Select options and perform actions
        select_options_and_search(driver, index)

        # Logout process
        user_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(@data-original-title, '')]"))
        )
        driver.execute_script("arguments[0].click();", user_dropdown)
        print("Clicked user dropdown")

        time.sleep(2)  # Wait for the dropdown to expand

        logout_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'logout')]"))
        )
        driver.execute_script("arguments[0].click();", logout_link)
        print("Clicked Logout link")

        # After logout, return to the login page for the next login
        driver.get("https://services.gst.gov.in/services/login")
        print("Navigating back to the login page.")

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Browser will remain open. Close it manually when done.")


# Function to read the input file and process each line
with open('input.txt', 'r') as file:
    # Set up Chrome WebDriver once
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    for line in file:
        username, password, index = line.strip().split(',')

        # Call gst_login with username, password, and index (use the same driver instance)
        print(f"Logging in with username: {username} for index {index}")
        # File handling: Create a file if it doesn't exist
        downloads_path = str(Path.home() / "Downloads")  # Get the Downloads folder
        user_folder_path = os.path.join(str(Path.home() / "Downloads"), f"{username}_gst")

        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
            print(f"Folder created: {user_folder_path}")
        else:
            print(f"Folder already exists: {user_folder_path}")

        # Set up a custom download directory for each user
        downloads_path = str(Path.home() / "Downloads")  # Get the Downloads folder
        user_download_dir = os.path.join(downloads_path, f"{username}_gst")

        # Configure Chrome WebDriver options
        chrome_options = Options()
        prefs = {
        "download.default_directory": user_download_dir,  # Set default download directory
        "download.prompt_for_download": False,  # Disable download prompts
        "directory_upgrade": True,  # Allow overwriting files in the directory
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)

        gst_login(username.strip(), password.strip(), index, driver)

    # Close the driver when all operations are done
    driver.quit()

