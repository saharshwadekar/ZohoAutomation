import time
import os
import tempfile
import shutil
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
    
    # Generate a unique user-data directory
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")  # Specify unique user data directory

    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Disable sandboxing (necessary for CI environments)
    
    # Setup ChromeDriver (it will automatically download the appropriate driver using webdriver-manager)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    return driver, user_data_dir  # Return driver and user_data_dir to clean up later

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
    driver.get('https://people.zoho.in/dealermatix/zp#home/myspace/overview-actionlist')  #
    time.sleep(5)  # Wait for the page to load

    try:
        # Wait for the check-in button to be visible and clickable
        button = driver.find_element(By.xpath("//button[@id='ZPAtt_check_in_out']"))
        button.click()
        print(f"Check-in successful at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
    except Exception as e:
        print(f"Error while reading or clicking the button: {e}")

# Function to perform check-out at 7:45 PM IST
def check_out(driver):
    driver.get('https://people.zoho.in/dealermatix/zp#home/myspace/overview-actionlist')  #
    time.sleep(5)  # Wait for the page to load

    try:
        # Wait for the check-out button to be visible and clickable
        button = driver.find_element(By.xpath("//button[@id='ZPAtt_check_in_out']"))
        button.click()
        print(f"Check-out successful at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
    except Exception as e:
        print(f"Error while reading or clicking the button: {e}")

# Main function to log in and perform check-in or check-out
def main(action):
    driver, user_data_dir = get_driver()  # Setup the WebDriver and unique user data dir
    try:
        login_to_zoho(driver)  # Login to Zoho

        if action == 'checkin':
            print('Let\'s Checkin')
            check_in(driver)
        elif action == 'checkout':
            print('Let\'s Checkout')
            check_out(driver)
        else:
            print("Invalid action!")
    finally:
        driver.quit()  # Close the browser after the task is complete
        shutil.rmtree(user_data_dir)  # Clean up the temporary user data directory

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not action:
        print("Please specify 'checkin' or 'checkout' as an argument")
        sys.exit(1)

    main(action)
