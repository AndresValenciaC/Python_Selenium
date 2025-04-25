"""Test class for validating the complete e-commerce shopping flow.
This class contains tests that simulate a user's journey through the application,
from login to checkout completion."""
import time

import allure

from page_objects.cart_page import CartPage
from page_objects.checkout_complete_page import CheckoutCompletePage
from page_objects.checkout_information_page import CheckoutInformationPage
from page_objects.checkout_overview_page import CheckoutOverviewPage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from utilities.config import (FIRST_NAME, LAST_NAME, PASSWORD, USERNAME,
                              ZIP_CODE, get_driver)


@allure.epic("E-commerce Application - Performance Test")
@allure.feature("End-to-End Shopping Flow - Performance Metrics")
class TestEcommerceFlow:
    """Test class for validating the complete e-commerce shopping flow.
    This class contains tests that simulate a user's journey through the application,
    from login to checkout completion and measures the performance metrics."""

    def setup_method(self):
        """Setup method that initializes the WebDriver and page objects.
        This ensures a clean state for test execution."""
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_info_page = CheckoutInformationPage(self.driver)
        self.checkout_overview_page = CheckoutOverviewPage(self.driver)
        self.checkout_complete_page = CheckoutCompletePage(self.driver)
        self.timings: dict[str, float] = {}

    def teardown_method(self):
        """Cleanup method that runs after each test.
        Ensures proper cleanup of resources."""
        if hasattr(self, 'driver'):
            self.driver.quit()

    @staticmethod
    def _calculate_step_time(start: float, end: float) -> float:
        """Calculate the time taken for a step.

        Args:
            start (float): Start time of the step
            end (float): End time of the step

        Returns:
            float: Time difference in seconds
        """
        return end - start

    def _log_step_time(self, step_name: str, duration: float) -> None:
        """Log step timing to Allure report.

        Args:
            step_name (str): Name of the step
            duration (float): Duration of the step in seconds
        """
        self.timings[step_name] = duration
        allure.attach(
            f"{step_name}: {duration:.2f} seconds",
            name=f"{step_name} Duration",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Complete Shopping Flow Timing")
    @allure.description("Validates flow from login to checkout, measuring performance at each step")
    @allure.title("End-to-End Shopping Flow Test with Performance Metrics")
    def test_total_flow_time(self):
        """Test the complete e-commerce flow while measuring performance metrics.

        This test:
        1. Logs in to the application
        2. Adds random products to cart
        3. Proceeds through checkout pages
        4. Validates completion
        5. Measures and reports timing for each step

        Raises:
            AssertionError: If any step takes longer than expected or if the flow fails
        """
        with allure.step("Step TC001: Login to application"):
            start_time = time.time()
            self.login_page.open_page()
            self.login_page.enter_username(USERNAME)
            self.login_page.enter_password(PASSWORD)
            self.login_page.click_login_button()
            login_time = time.time()
            self._log_step_time("Login", self._calculate_step_time(start_time, login_time))

        with allure.step("Step TC002: Add products to cart"):
            self.product_page.wait_for_product_title()
            self.product_page.get_products_random_list()
            self.product_page.add_random_products_to_cart()
            product_time = time.time()
            self._log_step_time("Product_Selection", self._calculate_step_time(login_time, product_time))

        with allure.step("Step TC003: Navigate to cart and proceed"):
            self.product_page.navigate_to_cart_page()
            self.cart_page.wait_for_cart_title()
            self.cart_page.click_checkout_button()
            cart_time = time.time()
            self._log_step_time("Cart_Navigation", self._calculate_step_time(product_time, cart_time))

        with allure.step("Step TC004: Fill checkout information"):
            self.checkout_info_page.wait_for_checkout_information_title_confirmation()
            self.checkout_info_page.fill_information_form(FIRST_NAME, LAST_NAME, ZIP_CODE)
            self.checkout_info_page.click_continue_button()
            checkout_info_time = time.time()
            self._log_step_time("Checkout_Information", self._calculate_step_time(cart_time, checkout_info_time))

        with allure.step("Step TC005: Review and confirm order"):
            self.checkout_overview_page.wait_for_checkout_overview_title()
            self.checkout_overview_page.click_finish_button()
            checkout_overview_time = time.time()
            self._log_step_time("Order_Review", self._calculate_step_time(checkout_info_time, checkout_overview_time))

        with allure.step("Step 6: Verify order completion"):
            self.checkout_complete_page.wait_for_checkout_complete_title()
            self.checkout_complete_page.click_back_home_button()
            complete_time = time.time()
            self._log_step_time("Order_Completion", self._calculate_step_time(checkout_overview_time, complete_time))


        with allure.step("Step TC007: Verify Total Flow Time"):
            # Calculate and log total flow time
            self._log_step_time("Total_Flow_Time", self._calculate_step_time(start_time, complete_time))

        # Performance assertions with detailed messages
        with allure.step("Validate Tests Performance Time Metrics"):

            assert self.timings["Total_Flow_Time"] < 30, (
                f"Total flow time({self.timings['Total_Flow_Time']:.2f}) exceeded maximum allowed time of 30s"
            )

            assert self.timings["Login"] < 5, (
                f"Login time ({self.timings['Login']:.2f}s) exceeded maximum allowed time of 5s"
            )
            assert self.timings["Product_Selection"] < 3, (
                f"Product selection time ({self.timings['Product_Selection']:.2f}s) exceeded maximum allowed time of 3s"
            )
            assert self.timings["Cart_Navigation"] < 2, (
                f"Cart Navigation time ({self.timings['Cart_Navigation']:.2f}s) exceeded maximum allowed time of 2s"
            )
            assert self.timings["Checkout_Information"] < 3, (
                f"Checkout Information time ({self.timings['Checkout_Information']:.2f}s) exceeded maximum allowed time of 3s"
            )
            assert self.timings["Order_Review"] < 3, (
                f"Order Review time ({self.timings['Order_Review']:.2f}s) exceeded maximum allowed time of 3s"
            )
            assert self.timings["Order_Completion"] < 3, (
                f"Order Completion time ({self.timings['Order_Completion']:.2f}s) exceeded maximum allowed time of 3s"
            )

            # Log performance metrics as a test artifact
            performance_summary = "\n".join([
                f"{step}: {time:.2f}s"
                for step, time in self.timings.items()
            ])
            allure.attach(
                performance_summary,
                name="Performance Summary",
                attachment_type=allure.attachment_type.TEXT
            )
