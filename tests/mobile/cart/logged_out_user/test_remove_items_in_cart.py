import allure, pytest, random
from pages.model.header_page import HeaderPage
from pages.model.catalog_page import CatalogPage
from pages.model.product_page import ProductPage
from pages.model.cart_page import CartPage
from utils.json_file_reader import read_json_file


@allure.epic("UI Testing")
@allure.feature("Remove from Cart")
@allure.story("Logged out user can remove items from Cart Page.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "products", [pytest.param(read_json_file("single_items"), id="single_items")]
)
def test_remove_items(driver, products):
    header_page = HeaderPage(driver)
    catalog_page = CatalogPage(driver)
    product_page = ProductPage(driver)

    current_count: int = 1
    product_list = products["data"]
    for product_name in product_list:
        with allure.step(f"Select product '{product_name}'."):
            catalog_page.tap_product(product_name)

        with allure.step("Tap Add to cart"):
            product_page.tap_add_to_cart()

        with allure.step(f"Verify cart icon displays badge number {current_count}."):
            header_page.verify_cart_icon_badge_text_equal_to(str(current_count))

        with allure.step("Tap Menu icon then select Catalog."):
            header_page.navigate_to_product_catalog_screen()

        with allure.step(f"Verify cart icon displays badge number {current_count}."):
            header_page.verify_cart_icon_badge_text_equal_to(str(current_count))

        current_count += 1
    current_count = len(product_list)

    with allure.step("Tap Cart icon."):
        header_page.tap_cart_icon()

    cart_page = CartPage(driver)
    cart_page.wait_for_cart_page_to_load()

    random.shuffle(product_list)
    for product_name in product_list.copy():
        with allure.step(f"Tap - until product {product_name} is removed from the cart"):
            cart_page.scroll_to_product_title(product_name)
            cart_page.decrease_product_qty(product_name, 0)
            current_count -= 1

        with allure.step("Verify item is removed from cart"):
            cart_page.verify_product_is_in_cart(product_name, False)
            product_list.remove(product_name)

        if (current_count > 1):
            with allure.step(f"Verify total item count in cart is equal to {current_count}"):
                cart_page.verify_total_items_in_cart(current_count)
        else:
            break

    product_name = product_list[0]
    with allure.step(f"Tap Remove item button for the last product {product_name}"):
        cart_page.click_remove_item_button(product_name)

    with allure.step("Verify No items text and Go shopping button is displayed"):
        cart_page.verify_no_item_is_displayed()

    with allure.step("Verify Go shopping button is displayed"):
        cart_page.verify_go_shopping_button_is_displayed()
        
