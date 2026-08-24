import allure, pytest
from pages.model.header_page import HeaderPage
from pages.model.catalog_page import CatalogPage
from pages.model.product_page import ProductPage
from pages.model.cart_page import CartPage
from utils.json_file_reader import read_json_file


@allure.epic("UI Testing")
@allure.feature("Add to Cart")
@allure.story("Logged out user can add item/s to cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "products",
    [pytest.param(read_json_file("multiple_item_qty"), id="multiple_item_qty")],
)
def test_add_diff_items_diff_qty_to_cart(driver, products):

    header_page = HeaderPage(driver)
    product_page = ProductPage(driver)
    catalog_page = CatalogPage(driver)
    product_list = products["data"]
    current_count: int = 0
    for product in product_list:
        product_name = product["item_name"]
        product_qty = product["qty"]
        with allure.step(f"Select product '{product_name}'."):
            catalog_page.tap_product(product_name)

        with allure.step(f"Tap + until quantity is equal to {product_qty}."):
            product_page.increase_product_qty(product_qty)

        with allure.step("Tap Add to cart"):
            product_page.tap_add_to_cart()
            current_count += product_qty

        with allure.step(f"Verify cart icon displays badge number {current_count}."):
            header_page.verify_cart_icon_badge_text_equal_to(str(current_count))

        with allure.step("Tap Menu icon then select Catalog."):
            header_page.navigate_to_product_catalog_screen()

        with allure.step(f"Verify cart icon displays badge number {current_count}."):
            header_page.verify_cart_icon_badge_text_equal_to(str(current_count))

    with allure.step("Tap Cart icon."):
        header_page.tap_cart_icon()

    cart_page = CartPage(driver)
    cart_page.wait_for_cart_page_to_load()

    for product in product_list:
        product_name = product["item_name"]
        product_qty = product["qty"]
        with allure.step(f"Verify product {product_name} displayed in Cart page."):
            cart_page.verify_product_is_in_cart(product_name)

        with allure.step(f"Verify product quantity is equal to {product_qty}."):
            cart_page.verify_item_qty_is_equal_to(product_name, product_qty)

    with allure.step(f"Verify total item count is equal to {current_count}."):
        cart_page.verify_total_items_in_cart(current_count)
