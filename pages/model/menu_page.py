from pages.model.base_page import BasePage
from pages.locator.menu_locator import MenuLocator


class MenuPage(BasePage):

    def open_menu(self):
        self.wait_for_element_visible(MenuLocator.MENU_BUTTON)
        self.click_element(MenuLocator.MENU_BUTTON)

    def tap_login_menu_item(self):
        self.wait_for_element_visible(MenuLocator.LOGIN_MENU_ITEM)
        self.click_element(MenuLocator.LOGIN_MENU_ITEM)

    def navigate_to_login_screen(self):
        self.open_menu()
        self.tap_login_menu_item()

    def is_logout_menu_item_displayed(self):
        return self.is_element_displayed(MenuLocator.LOGOUT_MENU_ITEM)

