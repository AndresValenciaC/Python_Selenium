"""Checkout Complete Page"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from locators.checkout_locators import CheckoutLocators


class CheckoutCompletePage:
    """Checkout Complete Page"""

    def __init__(self, driver):
        self.driver = driver
        self.locators = CheckoutLocators()

    def wait_for_checkout_complete_title(self):
        """Wait for the checkout complete title"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.locators.CHECKOUT_PAGE_COMPLETE_TITLE)
        )

    def get_checkout_complete_title(self):
        """Get the checkout complete title"""
        return self.driver.find_element(
            *self.locators.CHECKOUT_PAGE_COMPLETE_TITLE
        ).text

    def get_thank_you_message(self):
        """Get the thank you message"""
        return self.driver.find_element(*self.locators.THANK_YOU_MESSAGE).text

    def click_back_home_button(self):
        """Click the back home button"""
        self.driver.find_element(*self.locators.BACK_HOME_BUTTON).click()
