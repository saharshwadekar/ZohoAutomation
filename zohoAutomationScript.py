import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytz
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fetch the email and password from environment variables (set in GitHub Secrets)
ZOHO_EMAIL = os.getenv('ZOHO_EMAIL')
ZOHO_PASSWORD = os.getenv('ZOHO_PASSWORD')

# Ensure the credentials are set
if not ZOHO_EMAIL or not ZOHO_PASSWORD:
    raise ValueError("Zoho email or password not set in environment variables.")

# Function to set up the Chrome WebDriver with headless mode
def get_driver():
    options = Options()
    options.add_argument("--headless")  # Headless mode (no UI)
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Disable sandboxing (necessary for CI environments)
    
    # Setup ChromeDriver (it will automatically download the appropriate driver using webdriver-manager)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to login to Zoho portal
def login_to_zoho(driver):
    driver.get('https://accounts.zoho.in/signin?servicename=zohopeople&signupurl=https://www.zoho.com/people/signup.html')
    time.sleep(2)  # Wait for page to load

    # Find the login fields and enter credentials
    email_field = driver.find_element(By.ID, "login_id")
    email_field.send_keys(ZOHO_EMAIL)
    email_field.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for the password field to load

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(ZOHO_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

    print("Successfully logged in!")

# Function to perform check-in at 9:45 AM IST
def check_in(driver):
    # Navigate to the Zoho check-in page (you will need the actual URL here)
    driver.get('https://people.zoho.in/dealermatix/zp#home/myspace/overview-actionlist')  # Replace with actual check-in URL

    time.sleep(5)  # Wait for the page to load

    # Wait until the check-in button is visible and clickable (increase timeout for better reliability)
    checkin_button = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ZPAtt_check_in_out"]'))  # Use XPath to locate the button
    )

    # Check the button text (Check-in or Check-out)
    try:
        button_text = checkin_button.find_element(By.XPATH, './div/p').text  # Get text inside <p> tag
        if button_text == "Check-in":
            checkin_button.click()
            print(f"Check-in successful at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
        else:
            print(f"Button state is '{button_text}'. No action taken.")
    except Exception as e:
        print(f"Error while reading the button text: {e}")

# Function to perform check-out at 7:45 PM IST
def check_out(driver):
    # Navigate to the Zoho check-out page (you will need the actual URL here)
    driver.get('https://people.zoho.in/dealermatix/zp#home/myspace/overview-actionlist')  # Replace with actual check-out URL

    time.sleep(5)  # Wait for the page to load

    # Wait until the check-out button is visible and clickable (increase timeout for better reliability)
    checkout_button = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ZPAtt_check_in_out"]'))  # Use XPath to locate the button
    )

    # Check the button text (Check-in or Check-out)
    try:
        button_text = checkout_button.find_element(By.XPATH, './div/p').text  # Get text inside <p> tag
        if button_text == "Check-out":
            checkout_button.click()
            print(f"Check-out successful at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
        else:
            print(f"Button state is '{button_text}'. No action taken.")
    except Exception as e:
        print(f"Error while reading the button text: {e}")

# Main function to log in and perform check-in or check-out
def main(action):
    driver = get_driver()  # Setup the WebDriver
    login_to_zoho(driver)  # Login to Zoho

    if action == 'checkin':
        check_in(driver)
    elif action == 'checkout':
        check_out(driver)
    else:
        print("Invalid action!")

    driver.quit()  # Close the browser after the task is complete

# Run the script for check-in or check-out based on an argument (this will be used by GitHub Actions)
if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not action:
        print("Please specify 'checkin' or 'checkout' as an argument")
        sys.exit(1)

    main(action)
