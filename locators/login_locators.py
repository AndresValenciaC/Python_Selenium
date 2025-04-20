"""
This module contains locators for the login page
"""

from selenium.webdriver.common.by import By
from utilities.config import LOGIN_URL


class LoginLocators:
    """Locators for the login page"""

    URL = LOGIN_URL
    # Locators for the login page
    LOGIN_PAGE_TITLE = (By.CSS_SELECTOR, "div[class='login_logo']")
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
