from appium.webdriver.common.appiumby import AppiumBy


class MenuLocator:

    MENU_BUTTON = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/menuIV"
    )

    LOGIN_MENU_ITEM = (
        AppiumBy.ACCESSIBILITY_ID,
        "Login Menu Item"
    )

    LOGOUT_MENU_ITEM = (
        AppiumBy.ACCESSIBILITY_ID,
        "Logout Menu Item"
    )
