from pages.model.base_page import BasePage
from pages.locator.product_locator import ProductLocator


class ProductPage(BasePage):

    def is_product_name_title_visible(self):
        return self.is_element_displayed(ProductLocator.PRODUCT_NAME_TITLE)

    def increase_product_qty(self, qty):
        self.scroll_to_product_qty()
        current_qty = int(self.get_element_text(ProductLocator.PRODUCT_QTY))
        for _ in range(current_qty, qty):
            self.click_element(ProductLocator.INCREASE_QTY)

    def decrease_product_qty(self, qty):
        self.scroll_to_product_qty()
        current_qty = int(self.get_element_text(ProductLocator.PRODUCT_QTY))
        for _ in range(current_qty, qty-1, -1):
            self.click_element(ProductLocator.DECREASE_QTY)

    def tap_add_to_cart(self):
        self.scroll_to_product_qty()
        self.click_element(ProductLocator.ADD_TO_CART)

    def scroll_to_product_qty(self):
        self.scroll_to_element_with_identifier(ProductLocator.SCROLL_TO_RESOURCE_ID, ProductLocator.PRODUCT_QTY[1])
    