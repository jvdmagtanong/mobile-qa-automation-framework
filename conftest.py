import subprocess, pytest, allure
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config import APPIUM_HOST, APPIUM_PORT, APK_PATH, DEVICE_NAME, DEVICE_UDID


@pytest.fixture
def driver():
    project_root = Path(__file__).parent
    app_path = project_root / APK_PATH
    package_name = "com.saucelabs.mydemoapp.android"

    package_check = subprocess.run(
        ["adb", "shell", "pm", "list", "packages", package_name],
        capture_output=True,
        text=True,
    )

    if package_name in package_check.stdout:
        subprocess.run(
            ["adb", "shell", "pm", "clear", package_name],
            check=True,
        )
    else:
        subprocess.run(
            ["adb", "install", "-r", str(app_path)],
            check=True,
        )

    options = UiAutomator2Options()
    options.load_capabilities(
        {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": DEVICE_NAME,
            "appium:udid": DEVICE_UDID,
            "appium:appPackage": package_name,
            "appium:appWaitActivity": f"{package_name}.view.activities.MainActivity",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:disableWindowAnimation": True,
            "appium:autoGrantPermissions": True,
            "appium:autoAcceptAlerts": True,
            # Force UiAutomator2 to ignore/dismiss System UI ANR dialogs automatically
            "appium:userWaitForDevice": False,
            "appium:flags": "--skip-unsupported-env-checks",
            # Skip background helper installation during session creation
            "appium:skipServerInstallation": False,
            "appium:skipDeviceInitialization": False,
            "appium:uiautomator2ServerInstallTimeout": 120000,
            "appium:uiautomator2ServerLaunchTimeout": 120000,
            "appium:appWaitDuration": 60000,
            "appium:adbExecTimeout": 120000,
        }
    )

    driver = webdriver.Remote(
        f"http://{APPIUM_HOST}:{APPIUM_PORT}",
        options=options,
    )

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
