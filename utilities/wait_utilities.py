from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""genera doc para prueba"""
class WaitUtilities:
    """Wait utilities"""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator: tuple, timeout: int = 10):
        """Wait for an element to be present on the page"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
