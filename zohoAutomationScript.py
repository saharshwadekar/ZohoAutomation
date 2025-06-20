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

# Fetch the email and password from environment variables
ZOHO_EMAIL = os.getenv('ZOHO_EMAIL')
ZOHO_PASSWORD = os.getenv('ZOHO_PASSWORD')

# Ensure credentials are set
if not ZOHO_EMAIL or not ZOHO_PASSWORD:
    raise ValueError("Zoho email or password not set in environment variables.")

# Function to set up Chrome WebDriver with headless mode and fake location
def get_driver():
    options = Options()
    options.add_argument("--headless=new")  # Use new headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Emulate location: Bharat Bhavan, Baner, Pune
    params = {
        "latitude": 18.5591,
        "longitude": 73.7864,
        "accuracy": 100
    }
    driver.execute_cdp_cmd("Page.enable", {})
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)

    return driver

# Function to log in to Zoho
def login_to_zoho(driver):
    driver.get('https://accounts.zoho.in/signin?servicename=zohopeople&signupurl=https://www.zoho.com/people/signup.html')
    time.sleep(2)  # Wait for page to load

    email_field = driver.find_element(By.ID, "login_id")
    email_field.send_keys(ZOHO_EMAIL)
    email_field.send_keys(Keys.RETURN)
    time.sleep(3)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(ZOHO_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(7)

    print("Successfully logged in.")

# Function to perform check-in
def check_in(driver):
    driver.get('https://people.zoho.in/dealermatix/zp#home/myspace/overview-actionlist')
    time.sleep(6)
    filename = f"zoho_page_now.html"
    output_path = os.path.join("output", filename)
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    print(f"✅ Page source saved to: {output_path}")
    try:
        button = driver.find_element(By.ID, "ZPAtt_check_in_out")
        button.click()
        print(f"✅ Check-in successful at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
    except Exception as e:
        print(f"❌ Check-in failed: {e}")

# Function to perform check-out
def check_out(driver):
    driver.get('https://people.zoho.in/dealermatix/zp#home/myspace/overview-actionlist')
    time.sleep(6)

    try:
        button = driver.find_element(By.ID, "ZPAtt_check_in_out")
        button.click()
        print(f"✅ Check-out successful at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
    except Exception as e:
        print(f"❌ Check-out failed: {e}")

# Main function
def main(action):
    driver = get_driver()
    try:
        login_to_zoho(driver)

        if action == 'checkin':
            print("📍 Attempting check-in...")
            check_in(driver)
        elif action == 'checkout':
            print("📍 Attempting check-out...")
            check_out(driver)
        else:
            print("⚠️ Invalid action! Use 'checkin' or 'checkout'.")
    finally:
        driver.quit()

# Entry point
if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else None

    if not action:
        print("⚠️ Please specify 'checkin' or 'checkout' as an argument")
        sys.exit(1)

    main(action)
