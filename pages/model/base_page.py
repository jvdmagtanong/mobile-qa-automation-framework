from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator) :
        return self.driver.find_element(*locator)

    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.click()

    def clear_and_enter_text(self, locator, text):
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def  get_element_text(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.text

    def is_element_displayed(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.is_displayed()

    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout) \
            .until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout) \
            .until(EC.element_to_be_clickable(locator))
