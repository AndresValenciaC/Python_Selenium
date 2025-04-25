"""
This module contains tests for the complete checkout process
Tests the information form, overview, and completion pages
"""

import allure
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
@allure.title("Setup Checkout Process")
def setup_checkout():
    """Setup fixture for checkout tests"""
    with allure.step("Initialize test setup"):
        driver = get_driver()
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        checkout_info_page = CheckoutInformationPage(driver)
        checkout_overview_page = CheckoutOverviewPage(driver)
        checkout_complete_page = CheckoutCompletePage(driver)

    with allure.step("Perform login and initial setup"):
        login_page.open_page()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="login_page",
            attachment_type=allure.attachment_type.PNG
        )
        login_page.enter_username(USERNAME)
        login_page.enter_password(PASSWORD)
        login_page.click_login_button()

        product_page.wait_for_product_title()
        product_page.get_products_random_list()
        product_page.add_random_products_to_cart()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="products_added",
            attachment_type=allure.attachment_type.PNG
        )

        product_page.navigate_to_cart_page()
        cart_page.wait_for_cart_title()
        cart_page.click_checkout_button()

    pages = {
        "driver": driver,
        "login_page": login_page,
        "product_page": product_page,
        "cart_page": cart_page,
        "checkout_info_page": checkout_info_page,
        "checkout_overview_page": checkout_overview_page,
        "checkout_complete_page": checkout_complete_page,
    }

    yield pages

    with allure.step("Cleanup test resources"):
        driver.quit()


@allure.epic("E-commerce Application")
@allure.feature("Checkout Process")
class BaseCheckoutTest:
    """Base class for checkout-related tests with shared setup"""

    @allure.step("Setup checkout process")
    def setup_checkout_process(
        self, setup_checkout, go_to_complete=False, start_from_info=True
    ):
        """Shared setup for checkout process"""
        checkout_info_page = setup_checkout["checkout_info_page"]
        if start_from_info:
            with allure.step("Fill checkout information"):
                checkout_info_page.fill_information_form(FIRST_NAME, LAST_NAME, ZIP_CODE)
                allure.attach(
                    f"First Name: {FIRST_NAME}\nLast Name: {LAST_NAME}\nZIP: {ZIP_CODE}",
                    name="checkout_info",
                    attachment_type=allure.attachment_type.TEXT
                )
                checkout_info_page.click_continue_button()

        checkout_overview_page = setup_checkout["checkout_overview_page"]
        with allure.step("Wait for overview page"):
            checkout_overview_page.wait_for_checkout_overview_title()

        if go_to_complete:
            with allure.step("Complete checkout process"):
                checkout_overview_page.click_finish_button()
                checkout_complete_page = setup_checkout["checkout_complete_page"]
                checkout_complete_page.wait_for_checkout_complete_title()
                return checkout_complete_page
        return checkout_overview_page


@allure.epic("E-commerce Application")
@allure.feature("Checkout Process")
@allure.story("Information Form")
class TestCheckoutInformationPage(BaseCheckoutTest):
    """Test suite for Checkout Information Page"""

    @allure.title("Verify Checkout Information Page Title")
    @allure.description("Validates that the checkout information page title is correctly displayed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_information_title(self, setup_checkout):
        """Test the checkout information page title it is visible"""
        checkout_info_page = setup_checkout["checkout_info_page"]

        with allure.step("Verify checkout information title"):
            checkout_info_page.wait_for_checkout_information_title_confirmation()
            title = checkout_info_page.get_checkout_information_title()
            assert title == "Checkout: Your Information"
            allure.attach(
                f"Page title: {title}",
                name="info_page_title",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"✅ Checkout information title verified: {title}")

    @allure.title("Test Information Form with Different Inputs")
    @allure.description("Validates the form with various input combinations including valid and invalid data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "first_name, last_name, zip_code, expected_result",
        [
            pytest.param(FIRST_NAME, LAST_NAME, ZIP_CODE, "success",
                        id="valid_information",
                        marks=allure.description("Test with valid user information")),
            pytest.param("", LAST_NAME, ZIP_CODE, "error",
                        id="missing_first_name",
                        marks=allure.description("Test with missing first name")),
            pytest.param(FIRST_NAME, "", ZIP_CODE, "error",
                        id="missing_last_name",
                        marks=allure.description("Test with missing last name")),
            pytest.param(FIRST_NAME, LAST_NAME, "", "error",
                        id="missing_zip_code",
                        marks=allure.description("Test with missing ZIP code")),
            pytest.param("", "", "", "error",
                        id="all_fields_empty",
                        marks=allure.description("Test with all fields empty")),
        ],
    )
    def test_fill_information_form(
        self, setup_checkout, first_name, last_name, zip_code, expected_result
    ):
        """Test filling the checkout information form with different input combinations"""
        checkout_info_page = setup_checkout["checkout_info_page"]

        with allure.step(f"Fill form with: {first_name}, {last_name}, {zip_code}"):
            checkout_info_page.fill_information_form(first_name, last_name, zip_code)
            allure.attach(
                f"First Name: {first_name}\nLast Name: {last_name}\nZIP: {zip_code}",
                name="form_inputs",
                attachment_type=allure.attachment_type.TEXT
            )
            checkout_info_page.click_continue_button()

        if expected_result == "success":
            with allure.step("Verify successful form submission"):
                checkout_overview_page = self.setup_checkout_process(
                    setup_checkout, start_from_info=False
                )
                title = checkout_overview_page.get_checkout_overview_title()
                assert title == "Checkout: Overview"
                print("✅ Form submitted successfully")
        else:
            with allure.step("Verify error message"):
                checkout_info_page.wait_for_error_message()
                error_message = checkout_info_page.get_error_message()
                allure.attach(
                    error_message,
                    name="error_message",
                    attachment_type=allure.attachment_type.TEXT
                )
                print(f"❌ Expected error - {error_message}")

                if not first_name:
                    assert "First Name is required" in error_message
                elif not last_name:
                    assert "Last Name is required" in error_message
                elif not zip_code:
                    assert "Postal Code is required" in error_message


@allure.epic("E-commerce Application")
@allure.feature("Checkout Process")
@allure.story("Order Overview")
class TestCheckoutOverviewPage(BaseCheckoutTest):
    """Test suite for Checkout Overview Page"""

    @allure.title("Verify Checkout Overview Page Title")
    @allure.description("Validates that the checkout overview page title is correctly displayed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_overview_title(self, setup_checkout):
        """Test the checkout overview page title it is visible"""
        with allure.step("Navigate to overview page and verify title"):
            checkout_overview_page = self.setup_checkout_process(
                setup_checkout, start_from_info=True
            )
            title = checkout_overview_page.get_checkout_overview_title()
            assert title == "Checkout: Overview"
            allure.attach(
                f"Page title: {title}",
                name="overview_title",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"✅ Overview page title verified: {title}")

    @allure.title("Validate Checkout Items Match Cart Items")
    @allure.description("Verifies that all items from cart are present in checkout overview")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_overview_items_validation(self, setup_checkout):
        """Test the checkout overview items validation"""
        cart_page = setup_checkout["cart_page"]

        with allure.step("Get cart items and checkout items"):
            checkout_overview_page = self.setup_checkout_process(
                setup_checkout, start_from_info=True
            )
            cart_items_names = cart_page.get_cart_product_name()
            checkout_items_names = checkout_overview_page.get_checkout_items_names()

            allure.attach(
                f"Cart items: {cart_items_names}\nCheckout items: {checkout_items_names}",
                name="items_comparison",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify items match"):
            assert len(cart_items_names) == len(checkout_items_names), \
                f"Items count mismatch: Cart({len(cart_items_names)}) vs Checkout({len(checkout_items_names)})"

            for cart_item in cart_items_names:
                assert cart_item in checkout_items_names, \
                    f"Item '{cart_item}' missing from checkout"
                print(f"✅ Verified item: {cart_item}")

    @allure.title("Verify Order Pricing Calculations")
    @allure.description("Validates all price calculations including subtotal, tax, and final total")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_items_prices(self, setup_checkout):
        """Items prices check"""
        with allure.step("Get all price information"):
            checkout_overview_page = self.setup_checkout_process(
                setup_checkout, start_from_info=True
            )
            checkout_items_prices = checkout_overview_page.get_checkout_items_prices()
            checkout_items_prices_sum = checkout_overview_page.sum_checkout_items_prices()
            checkout_items_sub_total = checkout_overview_page.get_sub_total_items()
            checkout_items_tax = checkout_overview_page.get_tax_total_items()
            checkout_items_total = checkout_overview_page.get_total_items()

            allure.attach(
                f"""Price Details:
                Individual Items: {checkout_items_prices}
                Calculated Sum: ${checkout_items_prices_sum:.2f}
                Subtotal: ${checkout_items_sub_total:.2f}
                Tax: ${checkout_items_tax:.2f}
                Total: ${checkout_items_total:.2f}""",
                name="price_details",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify price calculations"):
            assert checkout_items_prices_sum == checkout_items_sub_total, \
                f"Subtotal mismatch: {checkout_items_prices_sum} != {checkout_items_sub_total}"

            expected_total = checkout_items_sub_total + checkout_items_tax
            assert expected_total == checkout_items_total, \
                f"Total mismatch: {expected_total} != {checkout_items_total}"

            print("✅ All price calculations verified successfully")


@allure.epic("E-commerce Application")
@allure.feature("Checkout Process")
@allure.story("Order Completion")
class TestCheckoutCompletePage(BaseCheckoutTest):
    """Test suite for Checkout Complete Page"""

    @allure.title("Verify Order Completion")
    @allure.description("Validates the successful completion of an order and confirmation messages")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_complete_title(self, setup_checkout):
        """Test the checkout complete page title it is visible"""
        with allure.step("Complete checkout process"):
            checkout_complete_page = self.setup_checkout_process(
                setup_checkout, go_to_complete=True, start_from_info=True
            )

        with allure.step("Verify completion page title"):
            title = checkout_complete_page.get_checkout_complete_title()
            assert title == "Checkout: Complete!"
            allure.attach(
                f"Completion page title: {title}",
                name="complete_title",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify thank you message"):
            thank_you_msg = checkout_complete_page.get_thank_you_message()
            assert thank_you_msg == "Thank you for your order!"
            allure.attach(
                f"Thank you message: {thank_you_msg}",
                name="thank_you_message",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"✅ Order completed successfully: {thank_you_msg}")

        with allure.step("Return to home page"):
            checkout_complete_page.click_back_home_button()
            allure.attach(
                setup_checkout["driver"].get_screenshot_as_png(),
                name="back_to_home",
                attachment_type=allure.attachment_type.PNG
            )
