import allure, pytest
from pages.model.header_page import HeaderPage
from pages.model.catalog_page import CatalogPage
from pages.model.product_page import ProductPage
from pages.model.cart_page import CartPage
from utils.json_file_reader import get_pytest_param


@allure.epic("UI Testing")
@allure.feature("Add to Cart")
@allure.story("Logged out user can add item/s to cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("product", get_pytest_param("single_items"))
def test_add_single_item_to_cart(driver, product):

    with allure.step(f"Select product '{product}'."):
        catalog_page = CatalogPage(driver)
        catalog_page.tap_product(product)

    with allure.step("Tap Add to cart"):
        product_page = ProductPage(driver)
        product_page.tap_add_to_cart()

    with allure.step("Verify cart icon displays badge number 1."):
        header_page = HeaderPage(driver)
        header_page.verify_cart_icon_badge_text_equal_to("1")

    with allure.step("Tap Cart icon."):
        header_page.tap_cart_icon()

    with allure.step(f"Verify product {product} displayed in Cart page."):
        cart_page = CartPage(driver)
        cart_page.wait_for_cart_page_to_load()
        cart_page.verify_product_is_in_cart(product)

    with allure.step("Verify total item count is equal to 1."):
        cart_page.verify_total_items_in_cart(1)

