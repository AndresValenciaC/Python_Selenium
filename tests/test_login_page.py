"""
This module contains tests for the login page
"""

import allure
import pytest

from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from utilities.config import PASSWORD, USERNAME, get_driver


@pytest.mark.parametrize(
    "username, password, expected_result",
    [
        (USERNAME, PASSWORD, "success"),
        ("wrong_user", "wrong_pass", "error"),
        (USERNAME, "wrong_pass", "error"),
        ("wrong_user", PASSWORD, "error"),
    ],
)
@allure.title("Test Login Authentication")
@allure.description(
    "This test attempts to log into the website using a login and a password. Fails if any error happens."
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("Owner", "Andres Valencia")
@allure.link("https://www.saucedemo.com/", name="Swag Labs")
@allure.issue("AUTH-1")
@allure.testcase("1")
def test_login_scenarios(username, password, expected_result):
    """Test different login scenarios"""
    driver = get_driver()
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    try:
        login_page.open_page()
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login_button()

        if expected_result == "success":
            product_page.wait_for_product_title()
            assert product_page.get_product_title() == "Products"
            print(
                "✅ Test test_fill_information_form passed successfully from TestCheckoutInformationPage"
            )

        else:
            # Verify error message
            assert (
                login_page.get_error_message()
                == "Epic sadface: Username and password do not match any user in this service"
            )
            print(
                "❌ Test failed - Username and password do not match any user in this service"
            )
    finally:
        driver.quit()
