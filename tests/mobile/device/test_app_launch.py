import allure, pytest


@allure.epic("UI Testing")
@allure.feature("Device")
@allure.story("User launches the app")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.device
@pytest.mark.smoke
@pytest.mark.regression
def test_app_launch(driver):
    assert driver is not None

    