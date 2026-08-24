import allure, pytest
from pages.model.header_page import HeaderPage
from pages.model.catalog_page import CatalogPage
from pages.model.product_page import ProductPage
from pages.model.cart_page import CartPage
from pages.model.login_page import LoginPage
from utils.config import USERNAME, PASSWORD
from utils.json_file_reader import get_pytest_param


@allure.epic("UI Testing")
@allure.feature("Add to Cart")
@allure.story("Logged out user can add item/s to cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("product", get_pytest_param("multiple_item_qty"))
def test_add_multiple_quantities_to_cart(driver, product):

    with allure.step("Tap the menu and then select Login"):
        header_page = HeaderPage(driver)
        header_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login(USERNAME, PASSWORD)

    with allure.step("Verify Log Out item is displayed in the Menu"):
        header_page.open_menu()
        header_page.verify_logout_menu_item_is_displayed()
        header_page.dismiss_menu()

    product_name = product["item_name"]
    product_qty = product["qty"]
    with allure.step(f"Select product '{product_name}'."):
        catalog_page = CatalogPage(driver)
        catalog_page.tap_product(product_name)

    with allure.step(f"Tap + until quantity is equal to {product_qty}."):
        product_page = ProductPage(driver)
        product_page.increase_product_qty(product_qty)

    with allure.step("Tap Add to cart"):
        product_page.tap_add_to_cart()

    with allure.step(f"Verify cart icon displays badge number {product_qty}."):
        header_page = HeaderPage(driver)
        header_page.verify_cart_icon_badge_text_equal_to(str(product_qty))

    with allure.step("Tap Cart icon."):
        header_page.tap_cart_icon()
    
    with allure.step(f"Verify product {product} displayed in Cart page."):
        cart_page = CartPage(driver)
        cart_page.wait_for_cart_page_to_load()
        cart_page.verify_product_is_in_cart(product_name)

    with allure.step(f"Verify product quantity is equal to {product_qty}."):
        cart_page.verify_item_qty_is_equal_to(product_name, product_qty)

    with allure.step(f"Verify total item count is equal to {product_qty}."):
        cart_page.verify_total_items_in_cart(product_qty)

    with allure.step("Verify Log Out item is displayed in the Menu"):
        header_page.open_menu()
        header_page.verify_logout_menu_item_is_displayed()

        