
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time
def select_options_and_search(driver):
    try:


        for q_index in range(1):  # 0, 1, 2, 3

            fin_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "fin"))
            )
            select_fin = Select(fin_dropdown)
            select_fin.select_by_index(1)
            selected_fin = select_fin.first_selected_option.text
            print(f"Successfully selected financial year: {selected_fin}")

            time.sleep(3)

            quarter_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "quarter"))
            )
            select_quarter = Select(quarter_dropdown)


            select_quarter.select_by_index(q_index)
            selected_quarter = select_quarter.first_selected_option.text
            print(f"Selected quarter: {selected_quarter}")
            time.sleep(3)

            period_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "mon"))
            )
            select_period = Select(period_dropdown)

            for p_index in range(1,3):  # 0, 1, 2
                select_period.select_by_index(p_index)
                selected_period = select_period.first_selected_option.text
                print(f"Selected period: {selected_period}")
                time.sleep(3)

                search_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.srchbtn[type='submit']"))
                )
                search_button.click()
                print("Clicked Search button")
                time.sleep(10)

                view_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary smallbutton' and contains(@data-ng-click, 'page_rtp')]"))
                )
                driver.execute_script("arguments[0].click();", view_button)
                print("Clicked VIEW button")

                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary' and contains(@data-ng-click, 'generateNILGstr1Pdf')]"))
                )

                if download_button.is_displayed() and download_button.is_enabled():
                    driver.execute_script("arguments[0].click();", download_button)
                    print("Clicked DOWNLOAD FILED (PDF) button")
                    driver.back()
                    print("Navigated back to the previous page")
                else:
                    driver.back()
                    print("Navigated back to the previous page")

                #driver.back()
                #print("Navigated back to the previous page")

                search_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.srchbtn[type='submit']"))
                )

                ##############again reset drop down ###################
                time.sleep(3)
                fin_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "fin"))
                )
                select_fin = Select(fin_dropdown)
                select_fin.select_by_index(1)
                print("here")
                time.sleep(3)
                quarter_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "quarter"))
                )
                select_quarter = Select(quarter_dropdown)
                select_quarter.select_by_index(q_index)
                time.sleep(3)
                print("here2")
                period_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "mon"))
                )
                select_period = Select(period_dropdown)
                select_period.select_by_index(p_index)

                search_button.click()
                print("Clicked Search button")

                download_button = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary pull-right' and @data-ng-click='downloadGSTR3Bpdf()']"))
                )
                driver.execute_script("arguments[0].click();", download_button)
                print("Clicked Download button")

                time.sleep(5)

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
