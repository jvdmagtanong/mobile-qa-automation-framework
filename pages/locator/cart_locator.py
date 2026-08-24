from appium.webdriver.common.appiumby import AppiumBy
from pages.locator.base_locator import BaseLocator


class CartLocator(BaseLocator):
    CART_PAGE_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    NO_ITEM_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noItemTitleTV")
    COLOR_ICON = (AppiumBy.ACCESSIBILITY_ID, "Displays color of selected product")
    CART_SCROLLABLE_CONTAINER = (AppiumBy.ACCESSIBILITY_ID, "Manages scrolling of views in given screen")
    PRODUCT_TITLE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@resource-id='com.saucelabs.mydemoapp.android:id/titleTV' and @text='{}']",
    )
    ITEM_COUNT = (
        AppiumBy.XPATH,
        PRODUCT_TITLE[1] + "/../.."
        "//android.widget.TextView[@resource-id='com.saucelabs.mydemoapp.android:id/noTV']",
    )
    PLUS_ITEM_COUNT = (
        AppiumBy.XPATH,
        PRODUCT_TITLE[1] + "/../.."
        "//android.widget.ImageView[@content-desc='Increase item quantity']",
    )
    MINUS_ITEM_COUNT = (
        AppiumBy.XPATH,
        PRODUCT_TITLE[1] + "/../.."
        "//android.widget.ImageView[@content-desc='Decrease item quantity']",
    )
    REMOVE_ITEM_BTN = (
        AppiumBy.XPATH, 
        PRODUCT_TITLE[1] + "/../.."
        "//android.widget.TextView[@content-desc='Removes product from cart']"
    )
    TOTAL_ITEM_COUNT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/itemsTV")
    GO_SHOPPING_BTN = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/shoppingBt")
