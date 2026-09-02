from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def scroll_to_element_with_identifier(self, locator, identifier):
        formatted_locator = (locator[0], locator[1].format(identifier))
        self.find_element(formatted_locator)

    def scroll_element(self, scrollable_element, direction="down", percent=0.4):
        self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "elementId": scrollable_element.id,
                "direction": direction,
                "percent": percent,
            }
        )

    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.click()

    def clear_and_enter_text(self, locator, text):
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def swipe_element_left(self, locator, percent=0.8):
        self._swipe_element(locator, percent=percent)

    def swipe_element_right(self, locator, percent=0.8):
        self._swipe_element(locator, direction="right", percent=percent)

    def _swipe_element(self, locator, direction="left", percent=0.8):
        element = self.find_element(locator)
        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "elementId": element.id,
                "direction": direction,
                "percent": percent,
            },
        )

    def get_element_text(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.text

    def is_element_displayed(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.is_displayed()

    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
