"""
This module contains a function to select a random web element or elements
from a list of elements
"""

import random
from selenium.webdriver.common.by import By


def random_web_element(driver, locator):
    """
    Select a random web element from a list of web elements

    Args:
        driver: WebDriver instance
        locator: Tuple of locator strategy and value (e.g., (By.ID, "my-id"))

    """
    elements = driver.find_elements(*locator)
    total_elements = len(elements)

    # If there are no elements, return an empty list
    if total_elements == 0:
        return []

    # Generate a random number between 1 and total_elements
    random_count = random.randint(1, total_elements)

    return random.sample(elements, random_count)
