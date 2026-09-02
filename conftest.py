import time, pytest, allure
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config import APPIUM_HOST, APPIUM_PORT, APK_PATH, DEVICE_NAME, DEVICE_UDID


@pytest.fixture
def driver():
    project_root = Path(__file__).parent
    app_path = project_root / APK_PATH
    package_name = "com.saucelabs.mydemoapp.android"

    options = UiAutomator2Options()
    options.load_capabilities(
        {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": DEVICE_NAME,
            "appium:udid": DEVICE_UDID,
            "appium:app": str(app_path),
            "appium:appPackage": package_name,
            "appium:appWaitActivity": "*",
            "appium:appWaitPackage": package_name,
            "appium:appWaitDuration": 120000,
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:disableWindowAnimation": True,
            "appium:autoGrantPermissions": True,
            "appium:autoAcceptAlerts": True,
            "appium:ignoreHiddenApiPolicyError": True,
            "appium:skipUnlock": True,
            "appium:noReset": False,  # Ensures app state/cache is reset cleanly upon session creation
            "appium:fullReset": False,  # Prevents uninstallation/reinstallation overhead
            "appium:androidInstallTimeout": 180000,
            "appium:uiautomator2ServerInstallTimeout": 180000,
            "appium:uiautomator2ServerLaunchTimeout": 240000,
            "appium:adbExecTimeout": 240000,
            "appium:simpleIsVisibleCheck": True,
            "appium:ignoreUnimportantViews": True,
        }
    )

    driver = webdriver.Remote(
        f"http://{APPIUM_HOST}:{APPIUM_PORT}",
        options=options,
    )

    driver.update_settings(
        {
            "waitForIdleTimeout": 0,
            "actionAcknowledgmentTimeout": 0,
            "allowInvisibleElements": True,
        }
    )

    # Allow app splash transition to complete cleanly
    time.sleep(5)

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
