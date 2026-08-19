import allure
import pytest
from pages.model.login_page import LoginPage
from pages.model.menu_page import MenuPage
from utils.config import USERNAME, PASSWORD


@allure.epic("UI Testing")
@allure.feature("Authentication")
@allure.story("Valid Login")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(driver):
    with allure.step("Tap the menu and then select Login"):
        menu_page = MenuPage(driver)
        menu_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login(USERNAME, PASSWORD)

    with allure.step("Verify Log Out item is displayed in the Menu"):
        menu_page.open_menu()
        assert menu_page.is_logout_menu_item_displayed()


@allure.epic("UI Testing")
@allure.feature("Authentication")
@allure.story("Locked Out User")
@allure.severity(allure.severity_level.CRITICAL)
def test_locked_out_user(driver):
    with allure.step("Tap the menu and then select Login"):
        menu_page = MenuPage(driver)
        menu_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login("alice@example.com", PASSWORD)

    error_message = "Sorry this user has been locked out."
    with allure.step(f"Verify error message '{error_message}' is displayed."):
        assert login_page.is_password_error_message_equal_to(error_message)


@allure.epic("UI Testing")
@allure.feature("Authentication")
@allure.story("Invalid Password")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalid_password(driver):
    with allure.step("Tap the menu and then select Login"):
        menu_page = MenuPage(driver)
        menu_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login(USERNAME, "INVALIDPASSWORD")

    error_message = "Username and Password do not match."
    with allure.step(f"Verify error message '{error_message}' is displayed."):
        assert login_page.is_password_error_message_equal_to(error_message)
