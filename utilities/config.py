import os

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

config_path = os.path.join(os.path.dirname(__file__), "config.yml")
# Load config from YAML file
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

print(config_path)

# Config variables
LOGIN_URL = config["login_url"]
USERNAME = config["username"]
PASSWORD = config["password"]

# Config variables for checkout page information form
FIRST_NAME = config["first_name"]
LAST_NAME = config["last_name"]
ZIP_CODE = config["zip_code"]


def get_driver():
    """Get the driver"""
    chrome_options = webdriver.ChromeOptions()

    # Create a clean profile
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Disable password and form filling
    chrome_options.add_argument("--password-store=basic")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-infobars")

    # Disable automation flags
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Comprehensive preferences
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "autofill.profile_enabled": False,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.javascript": 1,
        "profile.default_content_setting_values.automatic_downloads": 1,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Create and configure the driver
    service = Service(executable_path="./drivers/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Execute CDP commands to disable features
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "deny"})
    driver.execute_cdp_cmd("Network.setBypassServiceWorker", {"bypass": True})

    # Set window size and position
    driver.maximize_window()
    return driver
