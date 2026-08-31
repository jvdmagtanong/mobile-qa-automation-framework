import subprocess, pytest, allure, time
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config import APPIUM_HOST, APPIUM_PORT, APK_PATH, DEVICE_NAME, DEVICE_UDID


@pytest.fixture
def driver():
    project_root = Path(__file__).parent
    app_path = project_root / APK_PATH
    package_name = "com.saucelabs.mydemoapp.android"

    # Pre-install APK directly via ADB
    subprocess.run(["adb", "install", "-r", "-g", str(app_path)], check=True)

    options = UiAutomator2Options()
    options.load_capabilities(
        {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": DEVICE_NAME,
            "appium:udid": DEVICE_UDID,
            "appium:appPackage": package_name,
            "appium:appActivity": f"{package_name}.view.activities.SplashActivity",
            "appium:appWaitActivity": f"{package_name}.view.activities.MainActivity",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:disableWindowAnimation": True,
            "appium:autoGrantPermissions": True,
            "appium:autoAcceptAlerts": True,
            "appium:ignoreHiddenApiPolicyError": True,
            "appium:uiautomator2ServerInstallTimeout": 120000,
            "appium:uiautomator2ServerLaunchTimeout": 120000,
            "appium:appWaitDuration": 60000,
            "appium:adbExecTimeout": 120000,
            # CRITICAL PERMANENT FIX: Pass server settings natively inside session creation payload
            "appium:settings": {
                "waitForIdleTimeout": 0,
                "actionAcknowledgmentTimeout": 0,
                "shouldAwaitFirstOnscreenFrame": False,
            },
        }
    )

    driver = webdriver.Remote(
        f"http://{APPIUM_HOST}:{APPIUM_PORT}",
        options=options,
    )

    # Re-enforce explicitly on active session
    driver.update_settings(
        {
            "waitForIdleTimeout": 0,
            "actionAcknowledgmentTimeout": 0,
            "shouldAwaitFirstOnscreenFrame": False,
        }
    )

    # Pause briefly for Splash -> Main Activity transition without keyevent hacks
    time.sleep(3)

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
