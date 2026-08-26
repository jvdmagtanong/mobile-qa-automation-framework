import subprocess, pytest, allure
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config import APPIUM_HOST, APPIUM_PORT, APK_PATH, DEVICE_NAME, DEVICE_UDID


@pytest.fixture
def driver():
    # Reset the app before every test
    subprocess.run(
        [
            "adb",
            "shell",
            "pm",
            "clear",
            "com.saucelabs.mydemoapp.android",
        ],
        check=True,
    )
    options = UiAutomator2Options()
    project_root = Path(__file__).parent
    app_path = project_root / APK_PATH

    options.load_capabilities(
        {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": DEVICE_NAME,
            "appium:udid": DEVICE_UDID,
            "appium:app": str(app_path),
            "appium:appWaitActivity": "com.saucelabs.mydemoapp.android.view.activities.MainActivity",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True,
        }
    )

    driver = webdriver.Remote(f"http://{APPIUM_HOST}:{APPIUM_PORT}", options=options)
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

            safe_name = item.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = screenshots_dir / f"{safe_name}.png"

            driver.save_screenshot(str(screenshot_path))

            allure.attach.file(
                str(screenshot_path),
                name=f"{item.name} - Failure Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
