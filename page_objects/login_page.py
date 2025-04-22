"""
This module contains the LoginPage class,
which is used to interact with the login page
"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from locators.login_locators import LoginLocators


class LoginPage:
    """Login page object"""

    def __init__(self, driver: WebDriver):
        """Initialize the login page object"""
        self.driver = driver
        self.locators = LoginLocators

    def open_page(self):
        """Open the login page"""
        self.driver.get(self.locators.URL)

    def enter_username(self, username):
        """Enter the username"""
        self.driver.find_element(*self.locators.USERNAME_INPUT).clear()
        self.driver.find_element(*self.locators.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        """Enter the password"""
        self.driver.find_element(*self.locators.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.locators.PASSWORD_INPUT).send_keys(password)

    def click_login_button(self):
        """Click the login button"""
        self.driver.find_element(*self.locators.LOGIN_BUTTON).click()

    def get_error_message(self):
        """Get the error message displayed on the login page"""
        try:
            error_element = self.driver.find_element(*self.locators.ERROR_MESSAGE)
            return error_element.text
        except NoSuchElementException:
            return ""
