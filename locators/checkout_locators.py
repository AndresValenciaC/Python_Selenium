"""Locators for the checkout pages"""

from selenium.webdriver.common.by import By


class CheckoutLocators:
    """Locators for the checkout pages"""

    # Checkout page Information Locators

    CHECKOUT_PAGE_INFORMATION_TITLE = (
        By.XPATH,
        "//span[@class='title' and text()='Checkout: Your Information']",
    )

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.XPATH, "//input[@data-test='continue']")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")

    # Checkout page Overview Locators

    CHECKOUT_PAGE_OVERVIEW_TITLE = (
        By.XPATH,
        "//span[@class='title' and text()='Checkout: Overview']",
    )

    CART_ITEM = (By.XPATH, "//div[@class='cart_item']")

    ITEM_QUANTITY = (By.XPATH, "//div[@class='cart_quantity']")
    ITEM_NAME = (By.XPATH, "//div[@data-test='inventory-item-name']")
    ITEM_DESCRIPTION = (By.XPATH, "//div[@data-test='inventory-item-desc']")
    ITEM_PRICE = (By.XPATH, "//div[@data-test='inventory-item-price']")
    # Price Total Section --------------------------------------
    ITEM_TOTAL = (By.XPATH, "//div[@data-test='subtotal-label']")
    TAX = (By.XPATH, "//div[@data-test='tax-label']")
    TOTAL = (By.XPATH, "//div[@class='summary_total_label']")
    # -----------------------------------------------------------

    FINISH_BUTTON = (By.XPATH, "//button[@data-test='finish']")

    # Checkout page Complete Locators

    CHECKOUT_PAGE_COMPLETE_TITLE = (
        By.XPATH,
        "//span[@data-test='title']",
    )

    THANK_YOU_MESSAGE = (By.XPATH, "//h2[@class='complete-header']")
    BACK_HOME_BUTTON = (By.XPATH, "//button[@data-test='back-to-products']")
