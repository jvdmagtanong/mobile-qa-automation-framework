from pages.locator.login_locator import LoginLocator
from pages.model.base_page import BasePage
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):

    def enter_username(self, username):
        self.clear_and_enter_text(LoginLocator.USERNAME_FIELD, username)

    def enter_password(self, password):
        self.clear_and_enter_text(LoginLocator.PASSWORD_FIELD, password)

    def tap_login(self):
        self.click_element(LoginLocator.LOGIN_BUTTON)

    def is_password_error_message_displayed(self):
        return self.is_element_displayed(LoginLocator.PASSWORD_ERROR_MESSAGE)

    def verify_password_error_message_is_equal_to(self, expected_message):
        try:
            assert self.get_element_text(LoginLocator.PASSWORD_ERROR_MESSAGE) == expected_message
        except TimeoutException:
            assert False

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.tap_login()

