"""
This module contains tests for the cart page
"""

import random
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from page_objects.cart_page import CartPage
from utilities.config import get_driver, USERNAME, PASSWORD


def test_remove_product_from_cart():
    """Test cart buttons by removing a random product from the cart"""
    driver = get_driver()
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    try:
        # Login
        login_page.open_page()
        login_page.enter_username(USERNAME)
        login_page.enter_password(PASSWORD)
        login_page.click_login_button()

        # Add products to cart
        product_page.get_products_random_list()

        product_page.add_random_products_to_cart()

        # Go to cart
        product_page.navigate_to_cart_page()
        cart_page.wait_for_cart_title()

        # Verify cart page title
        assert (
            cart_page.get_cart_title() == "Your Cart"
        ), "Cart page title is not correct"
        print(f"✅ Verified cart page title: {cart_page.get_cart_title()}")

        # Get initial cart state
        initial_products = cart_page.get_cart_product_name()
        assert len(initial_products) > 0, "No products in cart to test removal"
        print(
            f"✅ Initial {len(initial_products)}  products in cart: {initial_products}"
        )

        # Remove a product
        product_to_remove = random.choice(initial_products)
        print(f"Product to remove: {product_to_remove}")
        assert cart_page.remove_product_from_cart(
            product_to_remove
        ), f"Failed to remove product {product_to_remove}"

        # Verify product was removed
        final_products = cart_page.get_cart_product_name()
        assert (
            product_to_remove not in final_products
        ), f"Product {product_to_remove} was not removed from cart"
        assert (
            len(final_products) == len(initial_products) - 1
        ), "Cart count did not decrease by 1"
        print(f"✅ Final {len(final_products)} products in cart: {final_products}")
        print(f"✅ Product {product_to_remove} removed from {final_products}")
    finally:
        driver.quit()
