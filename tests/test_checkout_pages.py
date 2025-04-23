"""Test the checkout pages"""

import pytest

from page_objects.cart_page import CartPage
from page_objects.checkout_complete_page import CheckoutCompletePage
from page_objects.checkout_information_page import CheckoutInformationPage
from page_objects.checkout_overview_page import CheckoutOverviewPage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from utilities.config import (FIRST_NAME, LAST_NAME, PASSWORD, USERNAME,
                              ZIP_CODE, get_driver)


@pytest.fixture(scope="function")
def setup_checkout():
    """Setup fixture for checkout tests"""
    driver = get_driver()
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    checkout_info_page = CheckoutInformationPage(driver)
    checkout_overview_page = CheckoutOverviewPage(driver)
    checkout_complete_page = CheckoutCompletePage(driver)

    # Login and add products to cart
    login_page.open_page()
    login_page.enter_username(USERNAME)
    login_page.enter_password(PASSWORD)
    login_page.click_login_button()
    product_page.wait_for_product_title()
    product_page.get_products_random_list()
    product_page.add_random_products_to_cart()
    product_page.navigate_to_cart_page()
    cart_page.wait_for_cart_title()
    cart_page.click_checkout_button()

    yield {
        "driver": driver,
        "login_page": login_page,
        "product_page": product_page,
        "cart_page": cart_page,
        "checkout_info_page": checkout_info_page,
        "checkout_overview_page": checkout_overview_page,
        "checkout_complete_page": checkout_complete_page,
    }

    driver.quit()


class BaseCheckoutTest:
    """Base class for checkout-related tests with shared setup"""

    def setup_checkout_process(
        self, setup_checkout, go_to_complete=False, start_from_info=True
    ):
        """Shared setup for checkout process"""
        checkout_info_page = setup_checkout["checkout_info_page"]
        if start_from_info:
            checkout_info_page.fill_information_form(FIRST_NAME, LAST_NAME, ZIP_CODE)
            checkout_info_page.click_continue_button()

        checkout_overview_page = setup_checkout["checkout_overview_page"]
        checkout_overview_page.wait_for_checkout_overview_title()

        if go_to_complete:
            checkout_overview_page.click_finish_button()
            checkout_complete_page = setup_checkout["checkout_complete_page"]
            checkout_complete_page.wait_for_checkout_complete_title()
            return checkout_complete_page
        return checkout_overview_page


class TestCheckoutInformationPage(BaseCheckoutTest):
    """Test suite for Checkout Information Page"""

    def test_checkout_information_title(self, setup_checkout):
        """Test the checkout information page title it is visible"""
        checkout_info_page = setup_checkout["checkout_info_page"]
        checkout_info_page.wait_for_checkout_information_title_confirmation()
        assert (
            checkout_info_page.get_checkout_information_title()
            == "Checkout: Your Information"
        )
        print(
            f"✅ Test checkout information title passed successfully from TestCheckoutInformationPage - {checkout_info_page.get_checkout_information_title()}"
        )

    @pytest.mark.parametrize(
        "first_name, last_name, zip_code, expected_result",
        [
            (FIRST_NAME, LAST_NAME, ZIP_CODE, "success"),
            ("", LAST_NAME, ZIP_CODE, "error"),
            (FIRST_NAME, "", ZIP_CODE, "error"),
            (FIRST_NAME, LAST_NAME, "", "error"),
            ("", "", "", "error"),
        ],
    )
    def test_fill_information_form(
        self, setup_checkout, first_name, last_name, zip_code, expected_result
    ):
        """Test filling the checkout information form with different input combinations"""
        checkout_info_page = setup_checkout["checkout_info_page"]
        checkout_info_page.fill_information_form(first_name, last_name, zip_code)
        checkout_info_page.click_continue_button()

        if expected_result == "success":
            checkout_overview_page = self.setup_checkout_process(
                setup_checkout, start_from_info=False
            )
            assert (
                checkout_overview_page.get_checkout_overview_title()
                == "Checkout: Overview"
            )
            print(
                "✅ Test test_fill_information_form passed successfully from TestCheckoutInformationPage"
            )
        else:
            checkout_info_page.wait_for_error_message()
            error_message = checkout_info_page.get_error_message()
            print(f"❌ Test failed - Error message: {error_message}")
            if not first_name:
                assert (
                    "First Name is required" in error_message
                ), f"Expected 'First Name is required', got '{error_message}'"
            elif not last_name:
                assert (
                    "Last Name is required" in error_message
                ), f"Expected 'Last Name is required', got '{error_message}'"
            elif not zip_code:
                assert (
                    "Postal Code is required" in error_message
                ), f"Expected 'Postal Code is required', got '{error_message}'"


class TestCheckoutOverviewPage(BaseCheckoutTest):
    """Test suite for Checkout Overview Page"""

    def test_checkout_overview_title(self, setup_checkout):
        """Test the checkout overview page title it is visible"""
        print("test_checkout_overview_title function")
        checkout_overview_page = self.setup_checkout_process(
            setup_checkout, start_from_info=True
        )
        assert (
            checkout_overview_page.get_checkout_overview_title() == "Checkout: Overview"
        )
        print(
            "✅ Test test_checkout_overview_title passed successfully from TestCheckoutOverviewPage"
        )

    def test_checkout_overview_items_validation(self, setup_checkout):
        """Test the checkout overview items validation"""
        print("test_checkout_overview_items_validation function")
        cart_page = setup_checkout["cart_page"]
        checkout_overview_page = self.setup_checkout_process(
            setup_checkout, start_from_info=True
        )
        cart_items_names = cart_page.get_cart_product_name()
        checkout_items_names = checkout_overview_page.get_checkout_items_names()
        assert len(cart_items_names) == len(
            checkout_items_names
        ), f"Number of items in cart ({len(cart_items_names)}) does not match number in checkout ({len(checkout_items_names)})"
        print(
            f"✅ Test test_checkout_overview_items_validation passed successfully - {len(cart_items_names)} items in cart, {len(checkout_items_names)} in checkout"
        )
        for cart_item in cart_items_names:
            assert (
                cart_item in checkout_items_names
            ), f"Item '{cart_item}' from cart not found in checkout overview"
            print(
                f"✅ Item '{cart_item}' found in checkout overview - {checkout_items_names}"
            )

    def test_check_items_prices(self, setup_checkout):
        """Items prices check"""
        print("test_check_items_prices")
        checkout_overview_page = self.setup_checkout_process(
            setup_checkout, start_from_info=True
        )
        checkout_items_prices = checkout_overview_page.get_checkout_items_prices()
        checkout_items_prices_sum = checkout_overview_page.sum_checkout_items_prices()
        checkout_items_sub_total = checkout_overview_page.get_sub_total_items()
        checkout_items_tax = checkout_overview_page.get_tax_total_items()
        checkout_items_total = checkout_overview_page.get_total_items()
        print(f"Items prices: {checkout_items_prices}")
        print(f"Calculated sum of items: ${checkout_items_prices_sum:.2f}")
        print(f"Subtotal on page: ${checkout_items_sub_total:.2f}")
        print(f"Tax on page: ${checkout_items_tax:.2f}")
        print(f"Total on page: ${checkout_items_total:.2f}")
        assert (
            checkout_items_prices_sum == checkout_items_sub_total
        ), f"Sum mismatch: {checkout_items_prices_sum} != {checkout_items_sub_total}"
        expected_total = checkout_items_sub_total + checkout_items_tax
        assert (
            expected_total == checkout_items_total
        ), f"Total mismatch: {expected_total} != {checkout_items_total}"
        print(
            "✅ Test test_check_items_prices passed successfully - Prices, subtotal, tax, and total match"
        )


class TestCheckoutCompletePage(BaseCheckoutTest):
    """Test suite for Checkout Complete Page"""

    def test_checkout_complete_title(self, setup_checkout):
        """Test the checkout complete page title it is visible"""

        checkout_complete_page = self.setup_checkout_process(
            setup_checkout, go_to_complete=True, start_from_info=True
        )

        assert (
            checkout_complete_page.get_checkout_complete_title()
            == "Checkout: Complete!"
        )
        print(
            f"✅ Test test_checkout_complete_title passed successfully from TestCheckoutCompletePage - {checkout_complete_page.get_checkout_complete_title()}"
        )
        assert (
            checkout_complete_page.get_thank_you_message()
            == "Thank you for your order!"
        )
        print(
            f"✅ Test test_checkout_complete_thank_you_message passed successfully from TestCheckoutCompletePage - {checkout_complete_page.get_thank_you_message()}"
        )
        checkout_complete_page.click_back_home_button()
