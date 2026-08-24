from pages.model.base_page import BasePage
from pages.locator.cart_locator import CartLocator, BaseLocator
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class CartPage(BasePage):

    def increase_product_qty(self, product_name, qty):
        current_qty = self.get_item_quantity(product_name)
        locator = (
            CartLocator.PLUS_ITEM_COUNT[0],
            CartLocator.PLUS_ITEM_COUNT[1].format(product_name)
        )
        for _ in range(current_qty, qty):
            self.click_element(locator)

    def decrease_product_qty(self, product_name, qty):
        current_qty = self.get_item_quantity(product_name)
        locator = (
            CartLocator.MINUS_ITEM_COUNT[0],
            CartLocator.MINUS_ITEM_COUNT[1].format(product_name)
        )
        for _ in range(current_qty, qty, -1):
            self.click_element(locator)

    def click_remove_item_button(self, product_name):
        locator = (
            CartLocator.REMOVE_ITEM_BTN[0],
            CartLocator.REMOVE_ITEM_BTN[1].format(product_name)
        )
        self.scroll_cart_container(locator)
        self.click_element(locator)

    def scroll_to_product_title(self, product_name):
        self.scroll_to_element_with_identifier(BaseLocator.SCROLL_TO_TEXT, product_name)

    def scroll_cart_container(self, locator):
        cart_container = self.find_element(CartLocator.CART_SCROLLABLE_CONTAINER)
        for _ in range(3):
            try:
                self.is_element_displayed(locator)
                break
            except TimeoutException:
                self.scroll_element(cart_container, percent=0.5)

    def get_item_quantity(self, product_name):
        locator = (
            CartLocator.ITEM_COUNT[0],
            CartLocator.ITEM_COUNT[1].format(product_name)
        )
        self.scroll_cart_container(locator)
        return int(self.get_element_text(locator))

    def get_total_items_in_cart(self):
        total = self.get_element_text(CartLocator.TOTAL_ITEM_COUNT).strip(" Items")
        return int(total)

    def wait_for_cart_page_to_load(self):
        self.wait_for_element_visible(CartLocator.CART_PAGE_TITLE)

    def is_cart_page_title_visible(self):
        return self.is_element_displayed(CartLocator.CART_PAGE_TITLE)

    def is_product_in_cart(self, product_name):
        locator = (
            CartLocator.PRODUCT_TITLE[0],
            CartLocator.PRODUCT_TITLE[1].format(product_name)
        )
        self.scroll_to_product_title(product_name)
        return self.is_element_displayed(locator)

    def verify_product_is_in_cart(self, product_name, is_in_cart=True):
        try:
            if (is_in_cart):
                assert self.is_product_in_cart(product_name)
            else:
                assert not self.is_product_in_cart(product_name)
        except NoSuchElementException:
            assert not is_in_cart

    def verify_item_qty_is_equal_to(self, product_name, expected_qty):
        actual_qty = self.get_item_quantity(product_name)
        assert expected_qty == actual_qty

    def verify_total_items_in_cart(self, total_count):
        assert total_count == self.get_total_items_in_cart()

    def verify_no_item_is_displayed(self, is_displayed=True):
        try:
            if (is_displayed):
                assert self.is_element_displayed(CartLocator.NO_ITEM_TITLE)
            else:
                assert not self.is_element_displayed(CartLocator.NO_ITEM_TITLE)
        except TimeoutException:
            assert not is_displayed

    def verify_go_shopping_button_is_displayed(self, is_displayed=True):
        try:
            if (is_displayed):
                assert self.is_element_displayed(CartLocator.GO_SHOPPING_BTN)
            else:
                assert not self.is_element_displayed(CartLocator.GO_SHOPPING_BTN)
        except TimeoutException:
            assert not is_displayed

