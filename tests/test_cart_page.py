"""
This module contains tests for the cart page functionality
Tests the ability to add and remove products from the shopping cart
"""
import random

import allure
import pytest

from page_objects.cart_page import CartPage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from utilities.config import PASSWORD, USERNAME, get_driver


@allure.epic("E-commerce Application")
@allure.feature("Shopping Cart Management")
@allure.story("Remove Products from Cart")
@allure.title("Test Remove Product from Cart")
@allure.description("""
    Verification of cart product removal functionality:
    1. Login with valid credentials
    2. Add random products to cart
    3. Navigate to cart page
    4. Verify cart page is displayed correctly
    5. Remove a random product
    6. Verify product was successfully removed
""")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("cart", "remove_product", "smoke_test")
@allure.link("https://your-test-management-system/TC001", name="Test Case Link")
@allure.issue("JIRA-123")
@pytest.mark.cart
@pytest.mark.smoke
def test_remove_product_from_cart():
    """Test cart functionality by removing a random product from the cart"""
    driver = get_driver()
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    try:
        # Login steps
        with allure.step("Login to the application"):
            login_page.open_page()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="login_page",
                attachment_type=allure.attachment_type.PNG
            )
            login_page.enter_username(USERNAME)
            login_page.enter_password(PASSWORD)
            login_page.click_login_button()

        # Add products to cart
        with allure.step("Add random products to cart"):
            product_page.get_products_random_list()
            product_page.add_random_products_to_cart()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="products_added",
                attachment_type=allure.attachment_type.PNG
            )

        # Navigate to cart
        with allure.step("Navigate to cart page"):
            product_page.navigate_to_cart_page()
            cart_page.wait_for_cart_title()

        # Verify cart page title
        @allure.step("Verify cart page title is correct")
        def verify_cart_title():
            assert cart_page.get_cart_title() == "Your Cart", "Cart page title is not correct"
            print(f"✅ Verified cart page title: {cart_page.get_cart_title()}")
            allure.attach(
                str(cart_page.get_cart_title()),
                name="cart_title",
                attachment_type=allure.attachment_type.TEXT
            )

        verify_cart_title()

        # Get initial cart state
        with allure.step("Get initial cart products"):
            initial_products = cart_page.get_cart_product_name()
            assert len(initial_products) > 0, "No products in cart to test removal"
            print(f"✅ Initial {len(initial_products)} products in cart: {initial_products}")
            allure.attach(
                str(initial_products),
                name="initial_cart_products",
                attachment_type=allure.attachment_type.TEXT
            )

        # Remove a product
        with allure.step("Remove random product from cart"):
            product_to_remove = random.choice(initial_products)
            print(f"Product to remove: {product_to_remove}")
            allure.attach(
                f"Selected product to remove: {product_to_remove}",
                name="product_to_remove",
                attachment_type=allure.attachment_type.TEXT
            )
            assert cart_page.remove_product_from_cart(
                product_to_remove
            ), f"Failed to remove product {product_to_remove}"

        # Verify product removal
        with allure.step("Verify product was successfully removed"):
            final_products = cart_page.get_cart_product_name()
            assert (
                product_to_remove not in final_products
            ), f"Product {product_to_remove} was not removed from cart"
            assert (
                len(final_products) == len(initial_products) - 1
            ), "Cart count did not decrease by 1"
            print(f"✅ Final {len(final_products)} products in cart: {final_products}")
            print(f"✅ Product {product_to_remove} removed from {final_products}")
            allure.attach(
                str(final_products),
                name="final_cart_products",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                driver.get_screenshot_as_png(),
                name="final_cart_state",
                attachment_type=allure.attachment_type.PNG
            )

    finally:
        driver.quit()
