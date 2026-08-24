import allure
from pages.model.login_page import LoginPage
from pages.model.header_page import HeaderPage
from utils.config import PASSWORD


@allure.epic("UI Testing")
@allure.feature("Authentication")
@allure.story("User login")
@allure.severity(allure.severity_level.CRITICAL)
def test_locked_out_user(driver):
    with allure.step("Tap the menu and then select Login"):
        header_page = HeaderPage(driver)
        header_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login("alice@example.com", PASSWORD)

    error_message = "Sorry this user has been locked out."
    with allure.step(f"Verify error message '{error_message}' is displayed."):
        login_page.verify_password_error_message_is_equal_to(error_message)

