"""
This module contains locators for the product page
"""

from selenium.webdriver.common.by import By


class ProductLocators:
    """Locators for the product page"""

    APP_LOGO = (By.XPATH, "//div[@class='app_logo' and text()='Swag Labs']")
    PRODUCT_TITLE = (By.XPATH, "//span[@class='title' and text()='Products']")
    PRODUCT_LIST = (By.XPATH, "//div[@class='inventory_item']")
    PRODUCT_NAME = (
        By.CSS_SELECTOR,
        "div.inventory_item_name[data-test='inventory-item-name']",
    )
    PRODUCT_PRICE = (By.CSS_SELECTOR, "div.inventory_item_price")
    PRODUCT_ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    PRODUCT_REMOVE_BUTTON = (By.XPATH, "//button[text()='Remove']")
    SHOPPING_CART_BADGE = (By.ID, "shopping_cart_container")
