import os
import time
import random
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client
from dotenv import load_dotenv


#Env Variables
load_dotenv()


#Twilio Setup
accountId = os.getenv('ACCOUNT_ID') 
authToken = os.getenv('TWILIO_AUTH_TOKEN') 
twilioPhoneNumber = os.getenv('TWILIO_PHONE_NUMBER') 
phoneNumber = os.getenv('PHONE_NUMBER')
client = Client(accountId, authToken)


# URL to scrape
page = 'https://www.canadacomputers.com/en/search?s=RTX+5070+Ti'

# Chrome options for stealth
opt = uc.ChromeOptions()

opt.add_argument("--disable-blink-features=AutomationControlled")
opt.add_argument("--disable-popup-blocking")
opt.add_argument("--log-level=3")  # Suppress logs
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 1  # Allow location
})


# Start driver
driver = uc.Chrome(options=opt)
driver.get(page)
driver.implicitly_wait(10)

# Store location data- id_store
storeLocations = ['56', '57', '58', '72', '51']

# Random sleep times for human-like behavior
randomTime = random.uniform(1, 5)
scrollTime = random.uniform(1, 3)

print("Starting Script")
while True:
    for storeLocation in storeLocations:
        try:
            logging.info(f"Checking store location {storeLocation}...")
            # Click the store selection dropdown
            locator = driver.find_element(By.XPATH, '//*[@id="avails"]/li[2]/a')
            locator.click()
            time.sleep(0.5)
            # Click specific store location
            location = driver.find_element(By.CSS_SELECTOR, f'li[data-id_store="{storeLocation}"]')
            location.click()
            # Wait for overlay to disappear
            try:
                overlay = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "content-overlay"))
                )
                WebDriverWait(driver, 10).until(EC.staleness_of(overlay))
            except Exception as e:
                logging.warning(f"Overlay did not disappear in time: {e}")
            # Locate product list
            productList = driver.find_element(By.XPATH, '//*[@id="js-product-list"]/div[1]')
            childDivs = productList.find_elements(By.XPATH, './div')
            # Skip iteration if no products found
            if not childDivs:
                logging.info("No products found for this store. Moving to next store...")
                continue
            # Loop to check product availability
            for div in childDivs:
                divID = div.get_attribute('id')
                validIds = {"product_card_268823", "product_card_269441", "product_card_269440", "product_card_268304"}
                if divID in validIds:
                    #Checking for the specific products I want
                    try:
                        availableTag = div.find_element(By.CLASS_NAME, 'available-tag')
                        stockAvailable = availableTag.get_attribute('data-stock_availability_retail')
                        if stockAvailable and int(stockAvailable) >= 1:
                            nameElement = driver.find_element(By.XPATH, f'//*[@id="{divID}"]/article/div[1]/div[2]/h2/a')
                            name = nameElement.text
                            logging.info(f"Product {divID} is available! Sending notification...")
                            message = client.messages.create(
                                body=f"{name} is available! Reply 'restart' to restart the loop or 'pause' to stop the script.",
                                from_=twilioPhoneNumber,
                                to=phoneNumber
                            )
                            with open("incomingMessage.txt", "w") as file:
                                file.write("")
                            while True: 
                                time.sleep(5)
                                try:
                                    with open("incomingMessage.txt", "r") as file:
                                        userInput = file.read().strip().lower()
                                        if userInput == 'restart':
                                            logging.info("Restarting script...")
                                            break
                                        elif userInput == 'pause':
                                            logging.info("Pausing script...")
                                except FileNotFoundError:
                                    continue                                
                        else:
                            logging.info(f"Product {divID} is NOT available.")
                    except NoSuchElementException:
                        logging.warning("Element with class 'available-tag' not found in this div.")
                        continue
        except Exception as e:
            logging.error(f"Error checking store {storeLocation}: {e}")
            continue