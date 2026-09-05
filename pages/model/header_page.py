from selenium.common import TimeoutException
from pages.model.base_page import BasePage
from pages.locator.header_locator import HeaderLocator


class HeaderPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_app_ready()

    def wait_for_app_ready(self):
        # CI emulators can take longer for the Android accessibility
        # hierarchy to become ready after the app launches.
        self.wait_for_element_clickable(HeaderLocator.MENU_BUTTON, timeout=30)

    def open_menu(self):
        self.wait_for_element_visible(HeaderLocator.MENU_BUTTON)
        self.click_element(HeaderLocator.MENU_BUTTON)

    def dismiss_menu(self):
        try:
            self.swipe_element_left(HeaderLocator.MENU_LIST_CONTAINER)
            self.wait_for_element_not_visible(HeaderLocator.MENU_LIST_CONTAINER)
        except TimeoutException:
            self.tap_cart_icon()
            self.wait_for_element_not_visible(HeaderLocator.MENU_LIST_CONTAINER)

    def tap_login_menu_item(self):
        self.wait_for_element_visible(HeaderLocator.LOGIN_MENU_ITEM)
        self.click_element(HeaderLocator.LOGIN_MENU_ITEM)

    def navigate_to_product_catalog_screen(self):
        self.open_menu()
        self.click_element(HeaderLocator.CATALOG_MENU_ITEM)

    def navigate_to_login_screen(self):
        self.open_menu()
        self.tap_login_menu_item()

    def tap_cart_icon(self):
        self.click_element(HeaderLocator.CART_ICON)

    def is_logout_menu_item_displayed(self):
        return self.is_element_displayed(HeaderLocator.LOGOUT_MENU_ITEM)

    def verify_cart_icon_badge_text_equal_to(self, count):
        badge_text = self.get_element_text(HeaderLocator.CART_BADGE)
        assert count == badge_text

    def verify_logout_menu_item_is_displayed(self, is_displayed=True):
        if (is_displayed):
            assert self.is_logout_menu_item_displayed()
        else:
            assert not self.is_logout_menu_item_displayed()

