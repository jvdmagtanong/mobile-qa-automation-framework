import allure, pytest
from pages.model.header_page import HeaderPage
from pages.model.catalog_page import CatalogPage
from pages.model.product_page import ProductPage
from pages.model.cart_page import CartPage
from pages.model.login_page import LoginPage
from utils.config import USERNAME, PASSWORD
from utils.json_file_reader import read_json_file


@allure.epic("UI Testing")
@allure.feature("Add to Cart")
@allure.story("Logged out user can add item/s to cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "products", [pytest.param(read_json_file("single_items"), id="single_items")]
)
def test_add_multiple_items_to_cart(driver, products):
    header_page = HeaderPage(driver)
    catalog_page = CatalogPage(driver)
    product_page = ProductPage(driver)

    with allure.step("Tap the menu and then select Login"):
        header_page.navigate_to_login_screen()

    with allure.step("Enter username and password then tap Log In button"):
        login_page = LoginPage(driver)
        login_page.login(USERNAME, PASSWORD)

    with allure.step("Verify Log Out item is displayed in the Menu"):
        header_page.open_menu()
        header_page.verify_logout_menu_item_is_displayed()
        header_page.dismiss_menu()
    
    item_count: int = 1
    product_list = products["data"]
    for product_name in product_list:
        with allure.step(f"Select product '{product_name}'."):
            catalog_page.tap_product(product_name)

        with allure.step("Tap Add to cart"):
            product_page.tap_add_to_cart()

        with allure.step(f"Verify cart icon displays badge number {item_count}."):
            header_page.verify_cart_icon_badge_text_equal_to(str(item_count))

        with allure.step("Tap Menu icon then select Catalog."):
            header_page.navigate_to_product_catalog_screen()

        with allure.step(f"Verify cart icon displays badge number {item_count}."):
            header_page.verify_cart_icon_badge_text_equal_to(str(item_count))

        item_count += 1
    item_count = len(product_list)

    with allure.step("Tap Cart icon."):
        header_page.tap_cart_icon()

    cart_page = CartPage(driver)
    cart_page.wait_for_cart_page_to_load()
    for product_name in product_list:
        with allure.step(f"Verify product {product_name} displayed in Cart page."):
            cart_page.verify_product_is_in_cart(product_name)

    with allure.step(f"Verify total item count is equal to {item_count}."):
        cart_page.verify_total_items_in_cart(item_count)
    
    with allure.step("Verify Log Out item is displayed in the Menu"):
        header_page.open_menu()
        header_page.verify_logout_menu_item_is_displayed()

