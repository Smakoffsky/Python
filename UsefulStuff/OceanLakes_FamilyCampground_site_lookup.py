import sys
import time
from datetime import datetime
import telebot
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

# Telegram bot configuration
CHAT_ID = -1023423448  # Telegram chat ID for notifications
TOKEN = '1733434AF7-BHrk_6oGktkWsdgfsdfriAW0ZH_Q'  # Telegram bot token
bot = telebot.TeleBot(TOKEN)  # Initialize Telegram bot

def send_telegram_message(message):
    """Send a message to the specified Telegram chat."""
    try:
        bot.send_message(CHAT_ID, message)
        # print(f"Telegram message sent: {message}")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def set_datepicker(driver, element_id, date):
    """Set the date for a datepicker element by ID."""
    try:
        datepicker = driver.find_element(By.ID, element_id)
        if not datepicker.is_displayed() or not datepicker.is_enabled():
            print(f"Datepicker {element_id} not interactable")
            return False
        datepicker.clear()
        datepicker.send_keys(date)
        print(f"Set {element_id} to {date}")
        return True
    except NoSuchElementException:
        print(f"Datepicker {element_id} not found")
        return False

def set_vehicle_length(driver, length):
    """Set the vehicle length in the specified input field."""
    try:
        vehicle_length = driver.find_element(By.ID, "VehicleLength")
        vehicle_length.clear()
        vehicle_length.send_keys(length)
        print(f"Set VehicleLength to {length}")
        return True
    except NoSuchElementException:
        print("VehicleLength input not found")
        return False

def set_checkbox(driver, element_id, check=True):
    """Set the checkbox to checked (or unchecked) by ID."""
    try:
        checkbox = driver.find_element(By.ID, element_id)
        if not checkbox.is_displayed() or not checkbox.is_enabled():
            print(f"Checkbox {element_id} not interactable")
            return False
        if checkbox.is_selected() != check:  # Only click if state needs to change
            checkbox.click()
            print(f"Checkbox {element_id} set to {'checked' if check else 'unchecked'}")
        else:
            print(f"Checkbox {element_id} already {'checked' if check else 'unchecked'}")
        return True
    except NoSuchElementException:
        print(f"Checkbox {element_id} not found")
        return False

def click_search_button(driver):
    """Click the search button using XPath."""
    try:
        search_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='search']")
        if not search_button.is_displayed() or not search_button.is_enabled():
            print("Search button not interactable")
            return False
        search_button.click()
        print("Search button clicked successfully")
        return True
    except (NoSuchElementException, ElementClickInterceptedException):
        print("Search button not found or not clickable")
        return False

def check_for_results(driver):
    """Check for 'no sites available' alert and return SectionCode values if sites are available."""
    try:
        # Check for no-results alert
        alert = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert.alert-info.text-center"))
        )
        expected_text = "There are no sites currently available that meet all of your search criteria"
        if expected_text in alert.text:
            print(f"Alert found with expected text: '{alert.text}'")
            # send_telegram_message(f"No sites available as of {datetime.now()}: {alert.text}")
            return False
        else:
            print(f"Alert text does not match. Found: '{alert.text}'")
    except TimeoutException:
        print("No alert found within 20 seconds, checking for SectionCode...")

    # Check for SectionCode elements
    try:
        elements = driver.find_elements(By.ID, "SectionCode")
        if elements:
            section_codes = [element.get_attribute("value") or element.text or "No value" for element in elements]
            print(f"SectionCode values found: {section_codes}")
            return section_codes
        else:
            print("No SectionCode elements found")
            return False
    except Exception as e:
        print(f"Error checking SectionCode: {e}")
        return False

def main():
    """Main function to execute the Selenium automation in an infinite loop."""
    try:
        # Initialize ChromeDriver with options to disable GPU
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-webgpu")
        chrome_options.add_argument("--log-level=1")
        # chrome_options.add_argument("--headless")  # Uncomment for headless mode
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_position(-10000, 0)
        print(f"Selenium version: {selenium.__version__}")

        # Send initial Telegram test message
        send_telegram_message("Started campsite search script")

        while True:  # Infinite loop until manually stopped
            try:
                # Navigate to the Ocean Lakes website
                driver.get("https://online.oceanlakes.com/")
                time.sleep(1)  # Wait for page to load

                # Set arrival date
                if not set_datepicker(driver, "startDatePicker", "07-02-2025"):
                    print("Failed to set arrival date, continuing to next iteration...")
                    send_telegram_message("Failed to set arrival date")
                    time.sleep(60)
                    continue

                time.sleep(1)  # Wait for UI stability

                # Set departure date
                if not set_datepicker(driver, "DepartureDate", "07-06-2025"):
                    print("Failed to set departure date, continuing to next iteration...")
                    send_telegram_message("Failed to set departure date")
                    time.sleep(60)
                    continue

                time.sleep(1)  # Wait for UI stability

                # Set vehicle length
                if not set_vehicle_length(driver, 31):
                    print("Failed to set vehicle length, continuing to next iteration...")
                    send_telegram_message("Failed to set vehicle length")
                    time.sleep(60)
                    continue

                time.sleep(1)  # Wait for UI stability

                # Set FrontSlideOut checkbox to unchecked
                if not set_checkbox(driver, "FrontSlideOut", False):
                    print("Failed to set FrontSlideOut checkbox, continuing to next iteration...")
                    send_telegram_message("Failed to set FrontSlideOut checkbox")
                    time.sleep(60)
                    continue

                time.sleep(1)  # Wait for UI stability

                # Click the search button
                if not click_search_button(driver):
                    print("Failed to click search button, continuing to next iteration...")
                    send_telegram_message("Failed to click search button")
                    time.sleep(60)
                    continue

                # Wait for search results and check for SectionCode values
                print("Checking for results...")
                section_codes = check_for_results(driver)
                if section_codes:
                    print("Sites may be available!")
                    codes_str = ", ".join(section_codes)
                    send_telegram_message(f"Sites may be available. SectionCode values: {codes_str}. Next check in 5 minutes.")
                    # sleep 5 mins after that
                    time.sleep(300)

                else:
                    print("No sites available, continuing...")

                # Wait before next iteration
                print("Waiting 20 seconds before next search...")
                time.sleep(20)

            except Exception as e:
                print(f"Unexpected error in loop: {e}")
                send_telegram_message(f"Unexpected error in loop: {e}")
                time.sleep(60)
                continue

    except KeyboardInterrupt:
        print("Script stopped manually by user")
        send_telegram_message("Campsite search script stopped manually")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        send_telegram_message(f"Script failed with error: {e}")
        sys.exit(1)
    finally:
        driver.quit()  # Ensure browser closes

if __name__ == "__main__":
    main()