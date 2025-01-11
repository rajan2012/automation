
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Example: Creating a WebDriver instance with an extended timeout
options = webdriver.ChromeOptions()

# Optional: Add more options if needed
options.add_argument("--start-maximized")

# Adjust desired capabilities
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal"  # Ensures full page load before timeout


def select_options_and_search(driver):
    try:
        for q_index in range(3,4):  # Iterate over quarters (adjust range as needed)
            # Select Financial Year
            fin_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "fin"))
            )
            select_fin = Select(fin_dropdown)
            select_fin.select_by_index(1)
            selected_fin = select_fin.first_selected_option.text
            print(f"Successfully selected financial year: {selected_fin}")
            time.sleep(3)

            # Select Quarter
            quarter_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "quarter"))
            )
            select_quarter = Select(quarter_dropdown)
            select_quarter.select_by_index(q_index)
            selected_quarter = select_quarter.first_selected_option.text
            print(f"Selected quarter: {selected_quarter}")
            time.sleep(3)

            # Select Period
            period_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "mon"))
            )
            select_period = Select(period_dropdown)
            for p_index in range(3):  # Iterate over periods (adjust range as needed)
                select_period.select_by_index(p_index)
                selected_period = select_period.first_selected_option.text
                print(f"Selected period: {selected_period}")
                time.sleep(3)

                # Click Search Button
                search_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.srchbtn[type='submit']"))
                )
                search_button.click()
                print("Clicked Search button")
                #time.sleep(7)

                # Handle View Button
                view_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary smallbutton' and contains(@data-ng-click, 'page_rtp')]"))
                )
                driver.execute_script("arguments[0].click();", view_button)
                print("Clicked VIEW button")

                try:
                    # Handle DOWNLOAD FILED (PDF) Button
                    download_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary' and contains(@data-ng-click, 'generateNILGstr1Pdf')]"))
                    )
                    driver.execute_script("arguments[0].click();", download_button)
                    print("Clicked DOWNLOAD FILED (PDF) button")
                    print(f"Download 2b view for 2023-2024,{selected_quarter},{selected_period}")
                    driver.back()
                    time.sleep(7)
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
                        print(f"Download 2b view summary for 2023-2024,{selected_quarter},{selected_period}")
                        driver.back()
                        time.sleep(3)
                        print("Navigated back to the previous page")
                        driver.back()
                        time.sleep(7)
                        print("Navigated back to the previous page")
                    except Exception as inner_exception:
                        print(f"Error in VIEW SUMMARY workflow: {inner_exception}")
                        time.sleep(5)

                time.sleep(10)
                # Ensure elements are reloaded
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.NAME, "fin"))
                )
                #time.sleep(10)
                # Reset dropdowns after navigation
                print("Resetting dropdown selections...")
                fin_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "fin"))
                )
                select_fin = Select(fin_dropdown)
                select_fin.select_by_index(1)
                print("Financial year reset")

                quarter_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "quarter"))
                )
                time.sleep(2)
                select_quarter = Select(quarter_dropdown)
                select_quarter.select_by_index(q_index)
                print("Quarter reset")
                time.sleep(2)

                period_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "mon"))
                )
                select_period = Select(period_dropdown)
                select_period.select_by_index(p_index)
                print("Period reset")

                search_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.srchbtn[type='submit']"))
                )
                search_button.click()
                print("Clicked Search button after reset")

                # Find and click the Download button
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//button[@class='btn btn-primary pull-right' and @data-ng-click='downloadGSTR3Bpdf()']"))
                )
                driver.execute_script("arguments[0].click();", download_button)
                print("Clicked Download button")
                print(f"Download 3b for {selected_fin},{selected_quarter},{selected_period}")
                time.sleep(7)



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

        login_button = WebDriverWait(driver, 30).until(
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

        time.sleep(3)

        #select_financial_year_quarter_and_period(driver)
        select_options_and_search(driver)




    except Exception as e:
        print(f"An error occurred: {e}")

    print("Browser will remain open. Close it manually when done.")


# Assuming you have already logged in and navigated to the correct page
# Call this function after successful login


gst_login()
