from appium.webdriver.common.appiumby import AppiumBy


class LoginLocator:

    # Login page
    USERNAME_FIELD = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/nameET"
    )

    PASSWORD_FIELD = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/passwordET"
    )

    LOGIN_BUTTON = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/loginBtn"
    )

    PASSWORD_ERROR_MESSAGE = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/passwordErrorTV"
    )

