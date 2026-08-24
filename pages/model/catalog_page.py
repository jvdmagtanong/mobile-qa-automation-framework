from pages.model.base_page import BasePage
from pages.locator.catalog_locator import CatalogLocator, BaseLocator


class CatalogPage(BasePage):

    def is_catalog_title_visible(self):
        return self.is_element_displayed(CatalogLocator.PRODUCT_CATALOG_TITLE)

    def tap_product(self, product_name):
        locator = (
            CatalogLocator.PRODUCT_IMAGE[0],
            CatalogLocator.PRODUCT_IMAGE[1].format(product_name)
        )
        self.scroll_to_element_with_identifier(BaseLocator.SCROLL_TO_TEXT, product_name)
        self.click_element(locator)


