"""
This module contains tests for the login authentication functionality
Tests different login scenarios with valid and invalid credentials
"""

import allure
import pytest

from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from utilities.config import PASSWORD, USERNAME, get_driver


@pytest.mark.parametrize(
    "username, password, expected_result",
    [
        pytest.param(
            USERNAME,
            PASSWORD,
            "success",
            id="valid_credentials",
            marks=[allure.description("Test login with valid username and password")]
        ),
        pytest.param(
            "wrong_user",
            "wrong_pass",
            "error",
            id="invalid_credentials",
            marks=[allure.description("Test login with invalid username and password")]
        ),
        pytest.param(
            USERNAME,
            "wrong_pass",
            "error",
            id="invalid_password",
            marks=[allure.description("Test login with valid username but invalid password")]
        ),
        pytest.param(
            "wrong_user",
            PASSWORD,
            "error",
            id="invalid_username",
            marks=[allure.description("Test login with invalid username but valid password")]
        ),
    ],
)
@allure.epic("E-commerce Application")
@allure.feature("User Authentication")
@allure.story("Login Authentication")
@allure.title("Test Login Authentication with Multiple Scenarios")
@allure.description("""
    Verification of login functionality with different credential combinations:
    1. Valid credentials (successful login)
    2. Invalid username and password
    3. Valid username with invalid password
    4. Invalid username with valid password

    Expected Results:
    - Success: User should be redirected to Products page
    - Error: Appropriate error message should be displayed
""")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("authentication", "login", "security", "smoke_test")
@allure.label("Owner", "Andres Valencia")
@allure.label("Layer", "UI")
@allure.label("Framework", "Selenium")
@allure.link("https://www.saucedemo.com/", name="Swag Labs")
@allure.issue("AUTH-1", "Authentication Test Cases")
@pytest.mark.login
@pytest.mark.smoke
def test_login_scenarios(username, password, expected_result):
    """Test different login scenarios with various credential combinations"""
    driver = get_driver()
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    try:
        with allure.step(f"Open login page for scenario: {username}"):
            login_page.open_page()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="login_page_initial",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step(f"Enter username: {username}"):
            login_page.enter_username(username)
            allure.attach(
                username,
                name="username_input",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Enter password"):
            login_page.enter_password(password)
            allure.attach(
                "********",  # Never log actual passwords
                name="password_input",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Click login button"):
            login_page.click_login_button()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="after_login_attempt",
                attachment_type=allure.attachment_type.PNG
            )

        if expected_result == "success":
            with allure.step("Verify successful login"):
                product_page.wait_for_product_title()
                title = product_page.get_product_title()
                assert title == "Products", f"Expected title 'Products' but got '{title}'"
                print("✅ Login successful - User redirected to Products page")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="products_page",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    f"Page title: {title}",
                    name="products_page_title",
                    attachment_type=allure.attachment_type.TEXT
                )

        else:
            with allure.step("Verify error message for failed login"):
                error_message = login_page.get_error_message()
                expected_error = "Epic sadface: Username and password do not match any user in this service"
                assert error_message == expected_error, f"Expected error message '{expected_error}' but got '{error_message}'"
                print(f"❌ Login failed as expected - {error_message}")
                allure.attach(
                    error_message,
                    name="error_message",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="error_state",
                    attachment_type=allure.attachment_type.PNG
                )

    except Exception as e:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="exception_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            str(e),
            name="exception_details",
            attachment_type=allure.attachment_type.TEXT
        )
        raise e

    finally:
        driver.quit()
