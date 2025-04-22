"""Page object for the cart page"""

import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.cart_products_locators import CartProductsLocators
from utilities.random_web_element_func import random_web_element


class CartPage:
    """Page object for the cart page"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.locators = CartProductsLocators

    def wait_for_cart_title(self):
        """Wait for the cart title to be visible"""
        self.driver.find_element(*self.locators.CART_PRODUCTS_TITLE)

    def get_cart_title(self):
        """Get the cart page title"""
        return self.driver.find_element(*self.locators.CART_PRODUCTS_TITLE).text

    def get_cart_product_name(self):
        """Get the cart product name or names"""
        cart_product_names = []
        for product in self.driver.find_elements(*self.locators.CART_PRODUCT_NAME):
            cart_product_names.append(product.text)
        # print(f"Cart products name in cart page: {cart_product_names}")
        return cart_product_names

    def remove_product_from_cart(self, product_name: str = None) -> bool:
        """
        Remove a product from the cart page and verify the removal

        Args:
            product_name: Name of the product to remove. If None, removes a random product

        Returns:
            bool: True if product was successfully removed, False otherwise
        """
        try:
            # Get current products in cart
            current_products = self.get_cart_product_name()
            if not current_products:
                print("No products in cart to remove")
                return False

            # Select product to remove
            if product_name is None:
                product_name = random.choice(current_products)
            # print(f"Random Product to remove in cart page: {product_name}")

            if product_name not in current_products:
                print(f"Product {product_name} not found in cart")
                return False

            # Format product name for selector
            formatted_name = product_name.lower().replace(" ", "-")
            # print(f"Formatted name in cart page: {formatted_name}")
            # Wait for and click remove button
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"button[data-test='remove-{formatted_name}']")
                )
            )
            remove_button.click()

            # Wait for product to be removed
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        f"//div[@data-test='inventory-item-name' and text()='{product_name}']",
                    )
                )
            )

            return True

        except Exception as e:
            print(f"Error removing product from cart: {str(e)}")
            return False

    def click_checkout_button(self):
        """Click the checkout button"""
        self.driver.find_element(*self.locators.CHECKOUT_BUTTON).click()
