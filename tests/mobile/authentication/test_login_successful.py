import allure
from pages.model.login_page import LoginPage
from pages.model.header_page import HeaderPage
from utils.config import USERNAME, PASSWORD


@allure.epic("UI Testing")
@allure.feature("Authentication")
@allure.story("User login")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(driver):
    with allure.step("Tap the menu and then select Login"):
        header_page = HeaderPage(driver)
        header_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login(USERNAME, PASSWORD)

    with allure.step("Verify Log Out item is displayed in the Menu"):
        header_page.open_menu()
        header_page.verify_logout_menu_item_is_displayed()

