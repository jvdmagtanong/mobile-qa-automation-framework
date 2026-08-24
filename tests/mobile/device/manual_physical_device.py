from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_physical_device():
    options = UiAutomator2Options()

    options.load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Redmi Note 9S",
        "appium:udid": "adb-b8e1a6-aWu5KL._adb-tls-connect._tcp",
        "appium:app": "/Users/Jover/Documents/QA-Portfolio/mobile-qa-automation-framework/apps/mda-2.2.0-25.apk",
    })

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options,
    )

    assert driver is not None

    driver.quit()