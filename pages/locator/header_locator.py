from appium.webdriver.common.appiumby import AppiumBy


class HeaderLocator:
    APP_LOGO_AND_NAME = (AppiumBy.ACCESSIBILITY_ID, "App logo and name")
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View menu")
    MENU_LIST_CONTAINER = (AppiumBy.ACCESSIBILITY_ID, "Recycler view for menu")
    CATALOG_MENU_ITEM = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Catalog")')
    LOGIN_MENU_ITEM = (AppiumBy.ACCESSIBILITY_ID, "Login Menu Item")
    LOGOUT_MENU_ITEM = (AppiumBy.ACCESSIBILITY_ID, "Logout Menu Item")
    CART_ICON = (AppiumBy.ACCESSIBILITY_ID, "Displays number of items in your cart")
    CART_BADGE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")

