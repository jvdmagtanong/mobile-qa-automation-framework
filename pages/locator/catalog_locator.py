from appium.webdriver.common.appiumby import AppiumBy
from pages.locator.base_locator import BaseLocator


class CatalogLocator(BaseLocator):
    PRODUCT_CATALOG_TITLE = (AppiumBy.ACCESSIBILITY_ID, "title")
    PRODUCT_IMAGE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@content-desc='Product Title' and @text='{}']"
        "/preceding-sibling::android.widget.ImageView[@content-desc='Product Image']",
    )
