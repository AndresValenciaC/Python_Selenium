"""Checkout Overview Page"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators.checkout_locators import CheckoutLocators


class CheckoutOverviewPage:
    """Checkout Overview Page"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.locators = CheckoutLocators

    def wait_for_checkout_overview_title(self):
        """Wait for the checkout overview title"""
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.locators.CHECKOUT_PAGE_OVERVIEW_TITLE)
        )

    def get_checkout_overview_title(self):
        """Get the checkout overview title"""
        return self.driver.find_element(
            *self.locators.CHECKOUT_PAGE_OVERVIEW_TITLE
        ).text

    def get_sub_total_items(self):
        """Get page subTotal from items prices"""
        sub_total = self.driver.find_element(*self.locators.ITEM_TOTAL).text
        return float(sub_total.replace("Item total: $", ""))

    def get_tax_total_items(self):
        """Get tax total from price items"""
        tax = self.driver.find_element(*self.locators.TAX).text
        return float(tax.replace("Tax: $", ""))

    def get_total_items(self):
        """Get total items"""
        total = self.driver.find_element(*self.locators.TOTAL).text
        return float(total.replace("Total: $", ""))

    def get_checkout_items_info(self):
        """Get the checkout items info"""
        checkout_items_info = []
        cart_items = self.driver.find_elements(*self.locators.CART_ITEM)

        for item in cart_items:
            item_quantity = item.find_element(By.CLASS_NAME, "cart_quantity").text
            item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            item_description = item.find_element(
                By.CLASS_NAME, "inventory_item_desc"
            ).text
            item_price = item.find_element(By.CLASS_NAME, "inventory_item_price").text

            checkout_items_info.append(
                {
                    "quantity": item_quantity,
                    "name": item_name,
                    "description": item_description,
                    "price": item_price,
                }
            )
        return checkout_items_info

    def get_checkout_items_names(self):
        """Get only the names of items in checkout overview"""
        return [item["name"] for item in self.get_checkout_items_info()]

    def get_checkout_items_prices(self):
        """Get the prices of items in checkout overview"""
        return [item["price"] for item in self.get_checkout_items_info()]

    def sum_checkout_items_prices(self):
        """Sum checkout items prices"""
        total = sum(
            float(item_price.replace("$", ""))
            for item_price in self.get_checkout_items_prices()
        )
        return total

    def click_finish_button(self):
        """Click the finish button"""
        self.driver.find_element(*self.locators.FINISH_BUTTON).click()
