"""
This module contains tests for the page products
"""

import allure
import pytest

from page_objects.cart_page import CartPage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from utilities.config import PASSWORD, USERNAME, get_driver


@pytest.fixture
def driver():
    """Fixture to initialize and return the driver"""
    driver = get_driver()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    """Fixture to initialize the login page"""
    return LoginPage(driver)


@pytest.fixture
def product_page(driver):
    """Fixture to initialize the product page"""
    return ProductPage(driver)


@pytest.fixture
def cart_page(driver):
    """Fixture to initialize the cart page"""
    return CartPage(driver)


@pytest.fixture
@allure.epic("E-commerce Application - Products Page")
@allure.feature("Products Page - Test Products Buttons and Add to Cart")
def logged_in_session(login_page, product_page):
    """Fixture to handle the login process"""
    login_page.open_page()
    login_page.enter_username(USERNAME)
    login_page.enter_password(PASSWORD)
    login_page.click_login_button()
    # Wait for products page to load
    product_page.wait_for_product_title()
    assert product_page.get_product_title() == "Products"
    print("✅ Products page title verified")
    return product_page

@allure.title("Test Products Buttons")
@allure.description("Test the products buttons selected in products page")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Test products page buttons")
@allure.testcase("1")
def test_products_btns(logged_in_session, product_page):
    """Test the products buttons selected in products page"""

    # Verify buttons text changes
    verification_results = product_page.verify_add_to_cart_buttons()

    # Assert we found products to test
    assert len(verification_results) > 0, "No products were found to test"
    print(f"✅ Found {len(verification_results)} products in test data")

    # Verify each button's text change
    for result in verification_results:
        product_name = result["product_name"]
        initial_text = result["initial_text"]
        final_text = result["final_text"]
        assert (
            result["initial_text"] == "Add to cart"
        ), f"Initial button text for {product_name} should be 'Add to cart', but was '{result['initial_text']}'"
        assert (
            result["final_text"] == "Remove"
        ), f"Button text for {product_name} should have changed to 'Remove', but was '{result['final_text']}'"
        print(
            f"✅ Successfully verified button {initial_text} -> {final_text} for {product_name}"
        )

@allure.title("Test Add Products to Cart")
@allure.description("Test adding products to cart")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Test adding products to cart")
@allure.testcase("2")
def test_add_products_to_cart(logged_in_session, product_page, cart_page):
    """Test adding products to cart"""

    # Select random products from products page
    product_page.get_products_random_list()

    # Get random product names in products page
    selected_products = product_page.get_random_products_name()

    # Add random products to cart in products page
    product_page.add_random_products_to_cart()

    # Navigate to cart page
    product_page.navigate_to_cart_page()

    # Wait for cart page to load
    cart_page.wait_for_cart_title()
    assert cart_page.get_cart_title() == "Your Cart"
    print("✅ Cart page title verified")

    # Get products from cart page
    cart_products = cart_page.get_cart_product_name()

    # Verify that the selected products from products page are in the cart page
    for product in selected_products:
        assert product in cart_products
        print(
            f"✅ Selected product- {product} from products page is in {cart_products} cart page"
        )
