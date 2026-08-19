import pytest
import allure
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture
def driver():
    options = UiAutomator2Options()
    project_root = Path(__file__).parent
    app_path = project_root/"apps"/"mda-2.2.0-25.apk"

    options.load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Pixel_10",
        "appium:udid": "emulator-5554",
        "appium:app": str(app_path),
        "appium:appWaitActivity": "com.saucelabs.mydemoapp.android.view.activities.MainActivity",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": False,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True,
    })

    driver = webdriver.Remote("http://127.0.0.1:4723",  options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")

        if driver:
            screenshots_dir = Path("test-reports/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = (
                screenshots_dir / f"{item.name}.png"
            )

            driver.save_screenshot(str(screenshot_path))

            allure.attach.file(
                str(screenshot_path),
                name=f"{item.name} - Failure Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

