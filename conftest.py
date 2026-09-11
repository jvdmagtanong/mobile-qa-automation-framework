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

    capabilities = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
    }

    options = UiAutomator2Options()
    options.load_capabilities(capabilities)

    options.device_name = DEVICE_NAME
    options.udid = DEVICE_UDID
    options.app = str(app_path)
    options.app_package = package_name
    options.app_wait_activity = "*"
    options.app_wait_package = package_name

    options.app_wait_duration = 120000
    options.android_install_timeout = 180000
    options.uiautomator2_server_install_timeout = 180000
    options.uiautomator2_server_launch_timeout = 240000
    options.adb_exec_timeout = 240000

    # Performance and UI optimizations
    options.disable_window_animation = True
    options.auto_grant_permissions = True
    options.ignore_hidden_api_policy_error = True
    options.skip_unlock = True
    options.no_reset = False

    driver = webdriver.Remote(
        f"http://{APPIUM_HOST}:{APPIUM_PORT}",
        options=options,
    )

    driver.update_settings(
        {
            "waitForIdleTimeout": 1000,
        }
    )

    driver.activate_app(package_name)
    # time.sleep(3)

    yield driver

    # Force-stop the app process before closing session
    try:
        driver.terminate_app(package_name)
    except Exception:
        pass

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
