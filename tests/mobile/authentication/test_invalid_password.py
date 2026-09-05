import allure
from pages.model.login_page import LoginPage
from pages.model.header_page import HeaderPage
from utils.config import USERNAME


@allure.epic("UI Testing")
@allure.feature("Authentication")
@allure.story("User login")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalid_password(driver):
    header_page = HeaderPage(driver)
    with allure.step("Tap the menu and then select Login"):
        header_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login(USERNAME, "INVALIDPASSWORD")

    error_message = "Username and Password do not match."
    with allure.step(f"Verify error message '{error_message}' is displayed."):
        login_page.verify_password_error_message_is_equal_to(error_message)

