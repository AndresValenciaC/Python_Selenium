"""
This module contains the ProductPage class,
which is used to interact with the product page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.product_locators import ProductLocators
from utilities.random_web_element_func import random_web_element


class ProductPage:
    """Product page object"""

    def __init__(self, driver: WebDriver):
        """Initialize the product page object"""
        self.driver = driver
        self.locators = ProductLocators
        self._random_products = []
        self._selected_product_names = []

    def wait_for_product_title(self):
        """Wait for product title"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.locators.APP_LOGO)
        )

    def get_product_title(self) -> str:
        """Get product title"""
        return self.driver.find_element(*ProductLocators.PRODUCT_TITLE).text

    def get_products_random_list(self) -> list:
        """Get random products from the products list"""
        self._random_products = random_web_element(
            self.driver, self.locators.PRODUCT_LIST
        )
        self._selected_product_names = []
        for product in self._random_products:
            product_name = product.find_element(*self.locators.PRODUCT_NAME).text
            self._selected_product_names.append(product_name)
        return self._random_products

    def get_random_products_name(self) -> list:
        """Get random products name from the random products list"""
        if not self._selected_product_names:
            self.get_products_random_list()
        # print(f"Random selected products in product_page: {self._random_products}")
        # print(f"Random_products_names in product_page: {self._selected_product_names}")
        return self._selected_product_names

    def add_random_products_to_cart(self):
        """Add random products to cart"""
        for product in self._random_products:
            # Get the product name and format it for the data-test attribute
            product_name = product.find_element(*self.locators.PRODUCT_NAME).text
            formatted_name = product_name.lower().replace(" ", "-")

            # Find and click the specific Add to Cart button for this product
            add_to_cart_button = product.find_element(
                By.CSS_SELECTOR, f"button[data-test='add-to-cart-{formatted_name}']"
            )
            add_to_cart_button.click()

            # Wait for the Remove button to appear for this specific product
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"button[data-test='remove-{formatted_name}']")
                )
            )
        # print(f"Added products to cart: {self._selected_product_names}")

    def navigate_to_cart_page(self):
        """Navigate to cart page"""
        cart = self.driver.find_element(*self.locators.SHOPPING_CART_BADGE)
        cart.click()

    def verify_add_to_cart_buttons(self) -> list:
        """Verify randomly that the Add to Cart button text
        change from Add to Cart to Remove when its clicked"""

        # Select a random products
        random_products = random_web_element(self.driver, self.locators.PRODUCT_LIST)
        print(f"Random products found: {len(random_products)} products")
        verification_results = []

        # For each random product, verify the button belongs to the product
        for product in random_products:
            product_name = product.find_element(*self.locators.PRODUCT_NAME).text
            formatted_name = product_name.lower().replace(" ", "-")
            add_to_cart_button = product.find_element(
                By.CSS_SELECTOR, f"button[data-test='add-to-cart-{formatted_name}']"
            )

            # Store initial button state
            initial_text = add_to_cart_button.text

            # Verify the button text change from Add to Cart to Remove when clicked
            if initial_text == "Add to cart":
                add_to_cart_button.click()
                remove_button = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            f"button[data-test='remove-{formatted_name}']",
                        )
                    )
                )
                final_text = remove_button.text
                verification_results.append(
                    {
                        "product_name": product_name,
                        "initial_text": initial_text,
                        "final_text": final_text,
                    }
                )
                # print(f"Verification Test results: {verification_results}")
            else:
                raise ValueError(
                    f"Button text is not Add to Cart: {add_to_cart_button.text}"
                )

        return verification_results
