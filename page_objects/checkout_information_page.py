"""Checkout Information Page"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators.checkout_locators import CheckoutLocators


class CheckoutInformationPage:
    """Checkout Information Page"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.locators = CheckoutLocators

    def wait_for_checkout_information_title_confirmation(self):
        """Wait for the checkout information title visibility and confirmation"""
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                self.locators.CHECKOUT_PAGE_INFORMATION_TITLE
            )
        )

    def get_checkout_information_title(self):
        """Get the checkout information title"""
        return self.driver.find_element(
            *self.locators.CHECKOUT_PAGE_INFORMATION_TITLE
        ).text

    def get_first_name_input(self):
        """Get the first name input"""
        return self.driver.find_element(*self.locators.FIRST_NAME_INPUT)

    def get_last_name_input(self):
        """Get the last name input"""
        return self.driver.find_element(*self.locators.LAST_NAME_INPUT)

    def get_zip_code_input(self):
        """Get the zip code input"""
        return self.driver.find_element(*self.locators.ZIP_CODE_INPUT)

    def fill_information_form(self, first_name, last_name, zip_code):
        """Fill the information form"""

        if first_name:
            self.get_first_name_input().send_keys(first_name)
        if last_name:
            self.get_last_name_input().send_keys(last_name)
        if zip_code:
            self.get_zip_code_input().send_keys(zip_code)

    def click_continue_button(self):
        """Click the continue button"""
        self.driver.find_element(*self.locators.CONTINUE_BUTTON).click()

    def wait_for_error_message(self):
        """Wait for the error message to be visible"""
        error_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.locators.ERROR_MESSAGE)
        )
        return error_message

    def get_error_message(self):
        """Get the error message"""
        return self.driver.find_element(*self.locators.ERROR_MESSAGE).text
