"""Locators for the cart products page"""

from selenium.webdriver.common.by import By


class CartProductsLocators:
    """Locators for the cart products page"""

    CART_PRODUCTS_TITLE = (By.XPATH, "//span[@class='title' and text()='Your Cart']")
    CART_PRODUCT_NAME = (
        By.CSS_SELECTOR,
        "div.inventory_item_name[data-test='inventory-item-name']",
    )
    CART_PRODUCT_QUANTITY = (By.CSS_SELECTOR, "div.cart_quantity")
    CART_PRODUCT_PRICE = (By.CSS_SELECTOR, "div.inventory_item_price")
    REMOVE_BUTTON = (By.XPATH, "//button[text()='Remove']")
    CHECKOUT_BUTTON = (By.XPATH, "//button[@data-test='checkout']")
