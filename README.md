# Mobile QA Automation Framework

This project is a mobile test automation framework built with Python, Appium, pytest, and Allure.

I created this project as part of my QA Automation / SDET portfolio to demonstrate my experience with mobile test automation, test framework design, automated reporting, and test environment setup.

The application used for testing is the Sauce Labs My Demo App for Android.

## Tech Stack

* Python
* Appium
* Appium Python Client
* Android Emulator
* UiAutomator2
* pytest
* Selenium WebDriver
* Allure
* python-dotenv
* Git / GitHub

## What This Framework Covers

The framework currently includes:

* Android mobile UI automation
* Appium with UiAutomator2
* Android emulator setup
* Page Object Model
* Separate locator and page model layers
* Reusable page actions
* pytest test execution
* Explicit waits for mobile elements
* Allure test reporting
* Allure test steps and test metadata
* Failure screenshots
* Test environment startup scripts
* Environment variables for configuration
* Support for both positive and negative login scenarios

## Framework Structure

The project is organized into separate areas for locators, page models, tests, configuration, and test environment setup.

```text
mobile-qa-automation-framework/
│
├── apps/
│   └── # APK is downloaded when needed and is not committed to Git
│
├── pages/
│   ├── locator/
│   │   ├── login_locator.py
│   │   └── menu_locator.py
│   │
│   └── model/
│       ├── base_page.py
│       ├── login_page.py
│       └── menu_page.py
│
├── scripts/
│   ├── start_appium.sh
│   ├── start_emulator.sh
│   └── start_test_environment.sh
│
├── tests/
│   └── mobile/
│       ├── test_app_launch.py
│       ├── test_login.py
│       └── manual_physical_device.py
│
├── utils/
│   └── config.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

# Framework Design

I separated the framework into a few simple layers.

## Locator Layer

The locator files contain the information needed to find elements in the application.

For example, the login locator file contains the locators for:

* Menu button
* Login menu item
* Username field
* Password field
* Login button
* Logout menu item
* Password error message

This keeps the element locators separate from the actions performed on those elements.

## Page Model Layer

The page model contains the actions that can be performed on each screen.

For example, the LoginPage contains actions such as:

* Open the menu
* Navigate to the Login screen
* Enter a username
* Enter a password
* Tap the Login button
* Verify that the Logout menu item is displayed
* Verify the password error message

The page models also use a reusable BasePage for common actions such as clicking elements, entering text, and waiting for elements to become visible or clickable.

## Test Layer

The test files contain the actual test scenarios.

The tests use the page models rather than directly interacting with Appium elements.

This makes the tests easier to read and keeps the test steps separate from the implementation details of the application.

### Why I Used a Base Page

The BasePage contains actions that are common to multiple pages.

For example:

* Finding an element
* Clicking an element
* Clearing and entering text
* Waiting for an element to become visible
* Waiting for an element to be clickable
* Getting the text from an element

Instead of repeating these methods in every page model, the other page models can reuse them.

### Explicit Waits

The framework uses explicit waits when interacting with elements.

For example, before reading the text of an error message, the framework waits for the element to become visible.

This is important in mobile automation because the application may still be changing screens or loading elements when the test tries to interact with them.

Using waits helps reduce timing-related test failures.

# Appium Driver Setup

The Appium driver is created in conftest.py using the Appium Python Client and Android UiAutomator2.

The current test environment uses:

* Platform: Android
* Automation engine: UiAutomator2
* Device: Pixel 10 Android Emulator
* Appium Server: 127.0.0.1:4723

The APK path is provided to Appium when the test session starts.

The driver is created for each pytest test and is closed after the test finishes.

# Android Emulator Setup

The project includes shell scripts to make starting the test environment easier.

## Start the emulator
```bash
./scripts/start_emulator.sh
```

This checks whether an Android emulator is already running. If it is not running, the script starts the configured emulator.

## Start Appium
```bash
./scripts/start_appium.sh
```

This checks whether an Appium server is already running.

If Appium is not running, the script starts it and waits until the server is ready.

## Start the complete test environment
```bash
./scripts/start_test_environment.sh
```

This starts the Android emulator and Appium server.

The goal is to keep environment setup separate from the test code.

## Running the Tests

After the Android emulator and Appium server are running, the tests can be executed with pytest.

For example:
```bash
pytest tests/mobile/test_login.py
```

To run all mobile tests:
```bash
pytest tests/mobile/
```

# Test Coverage

The current tests include application launch and authentication scenarios.

## Successful Login

The successful login test verifies that:

* The menu is opened.
* The Login option is selected.
* Valid credentials are entered.
* The Login button is tapped.
* The user is successfully logged in.
* The Logout menu item is displayed.

## Locked-Out User

The locked-out user test verifies that the application displays the expected error message when a locked-out user attempts to log in.

## Invalid Password

The invalid password test verifies the application's response when an incorrect password is entered.

This test also demonstrates how an incorrect expected result is reported as a failed test in Allure.

# Allure Reporting

Allure is used to provide a visual test report.

Test results are first generated by pytest:
```bash
pytest tests/mobile/test_login.py --alluredir=test-reports/allure-results
```

The Allure report can then be generated with:
```bash
allure generate test-reports/allure-results \
    -o test-reports/allure-report \
    --clean
```

The report can be opened with:
```bash
allure open test-reports/allure-report
```

The tests also use Allure metadata such as:

* Epic
* Feature
* Story
* Severity
* Test steps

This makes the test results easier to understand when reviewing them in the Allure report.

## Failure Screenshots

The framework automatically captures a screenshot when a test fails.

### The screenshot is:

Saved to the test reports directory.
Attached to the corresponding Allure test result.

This makes it easier to understand what was displayed on the mobile application at the time of failure.

The screenshot handling is implemented in the pytest test lifecycle rather than inside the page objects.

# Test Environment Configuration

Environment-specific values are kept outside of the test code.

The project uses environment variables and python-dotenv for local configuration.

Sensitive values such as passwords are not stored in the Git repository.

The ```.env``` file is excluded through ```.gitignore```.

# Application Under Test

This framework uses the Sauce Labs My Demo App for Android as the application under test.

The application provides a simple mobile shopping experience that is useful for demonstrating common mobile automation scenarios such as:

* Application launch
* Login
* Authentication errors
* Navigation
* Product interaction

The application is used only as a test application for this portfolio project.

The APK is not committed to this repository. It will be downloaded as part of the test environment setup when needed.

# Git and Repository Management

The project uses Git for source control.

The repository excludes files and folders that should not be committed, including:

* Python virtual environments
* .env files
* Python cache files
* pytest cache
* Allure-generated test reports
* VS Code settings
* Application binaries

The goal is to keep the repository focused on the automation framework source code and configuration.

# Current Status

The framework currently supports Android UI automation using Appium and pytest.

## Completed:

* Android emulator setup
* Appium server setup
* Appium driver configuration
* Page Object Model
* Locator layer
* Reusable base page
* Login page model
* Menu page model
* Login test scenarios
* Explicit waits
* Allure reporting
* Allure test metadata
* Failure screenshots
* Test environment startup scripts
* Git repository setup
* Next Steps

## Planned improvements include:

* Downloading the application APK automatically during test setup
* Adding more mobile test scenarios
* Expanding the page model and locator layers as new screens are tested
* Adding GitHub Actions for automated test execution
* Running the mobile tests in a CI environment
* Improving test execution and reporting as the framework grows

# Author

Jose Magtanong

QA Automation Engineer / SDET Portfolio Project