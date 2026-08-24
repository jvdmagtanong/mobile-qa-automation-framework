from appium.webdriver.common.appiumby import AppiumBy


class BaseLocator:
    SCROLL_TO_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().text("{}"))'
    )
    SCROLL_TO_RESOURCE_ID = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().resourceId("{}"))'
    )
