from appium.webdriver.common.appiumby import AppiumBy
from pages.locator.base_locator import BaseLocator


class ProductLocator(BaseLocator):
    PRODUCT_NAME_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    DECREASE_QTY = (AppiumBy.ACCESSIBILITY_ID, "Decrease item quantity")
    INCREASE_QTY = (AppiumBy.ACCESSIBILITY_ID, "Increase item quantity")
    PRODUCT_QTY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV")
    ADD_TO_CART = (AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart")
    SELECTED_COLOR = (
        AppiumBy.XPATH,
        "//android.widget.ImageView[@content-desc='Indicates when color is selected']"
        "/following-sibling::android.widget.ImageView",
    )
    SAUCE_LAB_BACKPACK_COLOR_BLACK = (AppiumBy.ACCESSIBILITY_ID, "Black color")
    SAUCE_LAB_BACKPACK_COLOR_BLUE = (AppiumBy.ACCESSIBILITY_ID, "Blue color")
    SAUCE_LAB_BACKPACK_COLOR_GRAY = (AppiumBy.ACCESSIBILITY_ID, "Gray color")
    SAUCE_LAB_BACKPACK_COLOR_GREEN = (AppiumBy.ACCESSIBILITY_ID, "Green color")
