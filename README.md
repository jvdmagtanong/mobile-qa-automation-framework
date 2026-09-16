# Mobile QA Automation Framework

This project is a mobile test automation framework built with Python, Appium, pytest, and Allure.

I created this project as part of my QA Automation / SDET portfolio to demonstrate mobile test automation, framework design, automated reporting, CI/CD, and AI-assisted test failure analysis.

The application used for testing is the Sauce Labs My Demo App for Android.

## Tech Stack

* Python 3.14
* Appium 3
* Appium Python Client
* Android Emulator
* Android UiAutomator2
* pytest
* Selenium WebDriver
* Allure
* Google Gemini API
* python-dotenv
* Git / GitHub
* GitHub Actions
* GitHub Pages

## What This Framework Covers

The framework currently includes:

* Android mobile UI automation
* Appium with UiAutomator2
* Android emulator setup
* Page Object Model
* Separate locator and page model layers
* Reusable BasePage actions
* pytest test execution and markers
* Explicit waits for mobile elements
* Allure test reporting
* Allure test steps and metadata
* Failure screenshots
* Sanitized Android UI hierarchy capture
* AI-assisted failure analysis using Google Gemini
* Test environment startup scripts
* Environment variables for configuration
* Positive and negative authentication scenarios
* GitHub Actions CI execution
* Allure reports published to GitHub Pages

## Framework Structure

The project is organized into separate areas for locators, page models, test data, tests, AI failure analysis, configuration, and test environment setup.

```text
mobile-qa-automation-framework/
│
├── .github/
│   └── workflows/
│       └── mobile-tests.yml
│
├── apps/
│   └── # APK is downloaded when needed and is not committed to Git
│
├── models/
│   └── failure_context.py
│
├── pages/
│   ├── locator/
│   │   ├── base_locator.py
│   │   ├── cart_locator.py
│   │   ├── catalog_locator.py
│   │   ├── header_locator.py
│   │   ├── login_locator.py
│   │   └── product_locator.py
│   │
│   └── model/
│       ├── base_page.py
│       ├── cart_page.py
│       ├── catalog_page.py
│       ├── header_page.py
│       ├── login_page.py
│       └── product_page.py
│
├── scripts/
│   ├── start_appium.sh
│   ├── start_emulator.sh
│   ├── start_test_environment.sh
│   └── workflow_run_tests.sh
│
├── tests/
│   ├── data/
│   │   ├── multiple_item_qty.json
│   │   └── single_items.json
│   │
│   └── mobile/
│       ├── authentication/
│       │   ├── test_invalid_password.py
│       │   ├── test_locked_out_user.py
│       │   └── test_login_successful.py
│       │
│       ├── cart/
│       │   ├── logged_in_user/
│       │   │   ├── test_add_diff_items_diff_qty_to_cart.py
│       │   │   ├── test_add_multiple_items_to_cart.py
│       │   │   ├── test_add_multiple_qty_to_cart.py
│       │   │   └── test_add_single_item_to_cart.py
│       │   │
│       │   └── logged_out_user/
│       │       ├── test_add_diff_items_diff_qty_to_cart.py
│       │       ├── test_add_multiple_items_to_cart.py
│       │       ├── test_add_multiple_qty_to_cart.py
│       │       ├── test_add_single_item_to_cart.py
│       │       ├── test_cart_qty_selector.py
│       │       └── test_remove_items_in_cart.py
│       │
│       └── device/
│           ├── manual_physical_device.py
│           └── test_app_launch.py
│
├── utils/
│   ├── allure_metadata.py
│   ├── config.py
│   ├── gemini_failure_analyzer.py
│   └── page_source_sanitizer.py
│
├── .gitignore
├── conftest.py
├── pytest.ini
├── requirements.txt
├── run_tests.sh
└── README.md
```

# Framework Design

The framework is divided into simple layers so that test scenarios remain readable while implementation details are kept reusable.

## Locator Layer

The locator files contain the information needed to find elements in the application.

For example, the login locator file contains locators for:

* Menu button
* Login menu item
* Username field
* Password field
* Login button
* Logout menu item
* Password error message

This keeps element locators separate from the actions performed on those elements.

## Page Model Layer

The page model contains the actions that can be performed on each screen.

The page models use a reusable BasePage for common actions such as finding elements, clicking, entering text, waiting for elements, and retrieving text.

The tests interact with page models rather than directly interacting with Appium elements. This keeps the test scenarios focused on functional behavior instead of implementation details.

## Test Layer

The test files contain the actual mobile test scenarios.

Tests use Allure metadata such as Epic, Feature, Story, Description, Severity, and test steps to provide functional context for both reporting and AI-assisted failure analysis.

## Failure Context

The `FailureContext` dataclass provides a single object containing the information needed for AI failure analysis, including:

* Test name
* Epic
* Feature
* Story
* Test description
* Stack trace
* Android UI hierarchy
* Framework information
* Device information
* Android version
* Appium version

This keeps the Gemini analyzer focused on analyzing a structured failure context rather than receiving a long list of unrelated arguments.

# AI-Assisted Failure Analysis

The framework uses Google Gemini to analyze failed mobile tests and provide automated root-cause analysis.

The analyzer combines the functional intent of the test with technical failure evidence rather than analyzing the stack trace alone.

The analysis can use:

* Test name
* Allure Epic, Feature, and Story
* Allure test description
* Failure stack trace
* Sanitized Android UI hierarchy
* Device information
* Android version
* Appium version

The Android UI hierarchy is sanitized before being sent to Gemini to remove unnecessary attributes and reduce noisy data while preserving useful information such as resource IDs, text, content descriptions, classes, and element state.

Gemini classifies failures into categories such as:

1. Application defect
2. Automation/test defect
3. Locator problem
4. Timing/synchronization issue
5. Appium/UiAutomator2 issue
6. Environment/device issue
7. Insufficient evidence

The analysis is attached to the corresponding Allure result as an **AI Failure Analysis** attachment.

The goal is not simply to identify the exception. The analyzer uses the test story and description to explain the expected functional behavior and then uses the technical evidence to explain how the observed behavior caused the failure.

<details>
<summary>### Sample Gemini Response:</summary>
1.  **Root Cause Summary**
    
    The test `test_invalid_password` failed because the application did not display the expected error message element after an attempt to log in with an invalid password. The functional expectation is that the user receives an appropriate error message, specifically "Username and Password do not match." However, the application did not render any element with the resource ID `com.saucelabs.mydemoapp.android:id/passwordErrorTV` on the screen. Consequently, the test automation framework timed out while waiting for this element to become visible, leading to an `AssertionError` that the "Password error message not found within the timeout period."

2.  **Failure Classification**

    Application defect

4.  **Evidence**
    *   **Test Description:** "Verify that a user receives an appropriate error message when attempting to log in with an invalid password." This sets the expectation for the application's behavior.
    *   **Stack Trace:** The `TimeoutException` clearly states, "Message: Element ('id', 'com.saucelabs.mydemoapp.android:id/passwordErrorTV') not visible after 10 seconds." This is immediately followed by a `NoSuchElementError` in the Appium stacktrace: "An element could not be located on the page using the given search parameters." This indicates the element was not present.
    *   **Sanitized Android UI Hierarchy:** A thorough review of the provided XML page source at the time of failure shows no element with the `resource-id="com.saucelabs.mydemoapp.android:id/passwordErrorTV"`. The expected error message element is entirely absent from the screen.
    *   **pytest.mark.xfail:** The test is marked with `@pytest.mark.xfail(reason="This test is expected to fail due a known issue.")`, which confirms that this is a recognized defect in the application's behavior.

5.  **Recommended Fix**

    The primary fix is within the application code. The development team needs to ensure that when a user attempts to log in with an invalid password, an error message element with the specified `resource-id` (`com.saucelabs.mydemoapp.android:id/passwordErrorTV`) is correctly displayed on the screen.

    If, upon investigation, the application *does* display an error message but uses a different element or locator, then the test automation should be updated to reflect the actual implementation. However, based on the current evidence, the element is entirely missing.

    *Example Application Code (Conceptual fix to display error):*

    ```java // Assuming Android Java/Kotlin for demonstration
    // In the LoginActivity or ViewModel after invalid login attempt
    if (!usernameIsValid || !passwordIsValid) {
        // Make the error TextView visible and set its text
        passwordErrorTextView.setVisibility(View.VISIBLE);
        passwordErrorTextView.setText("Username and Password do not match.");
        // Ensure this TextView has the ID com.saucelabs.mydemoapp.android:id/passwordErrorTV
    } else {
        // Hide the error TextView on successful login or other states
        passwordErrorTextView.setVisibility(View.GONE);
    }
    ```

7.  **Confidence Level**
    **High.** The combination of the `NoSuchElementError` reported by Appium, the `TimeoutException` for the element, and the explicit absence of the element's resource ID in the UI hierarchy dump provides conclusive evidence that the application failed to display the expected error message. The `xfail` marker further reinforces this as a known application defect.
</details>

# Appium Driver Setup

The Appium driver is created in `conftest.py` using the Appium Python Client and Android UiAutomator2.

The CI test environment currently uses:

* Platform: Android
* Android API: 30
* Device: Pixel 2 emulator
* Architecture: x86_64
* Automation engine: UiAutomator2
* Appium Server: 127.0.0.1:4723
* KVM hardware acceleration in GitHub Actions

The APK path is provided to Appium when the test session starts.

The driver is created for each pytest test and is closed after the test finishes.

# Local Environment Setup

## Prerequisites

Install the following before running the framework locally:

* Python 3.14
* Node.js / npm
* Appium 3
* Appium UiAutomator2 driver
* Android Studio
* Android SDK and emulator
* Allure Commandline
* Git

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Install Appium if it is not already installed:

```bash
npm install -g appium
```

Install the Android UiAutomator2 driver:

```bash
appium driver install uiautomator2
```

## Create the `.env` File

The framework uses `python-dotenv` to load local configuration from a `.env` file.

Create a `.env` file in the root of the project:

```bash
touch .env
```

Add the following values:

```dotenv
USERNAME=<valid-demo-app-username>
PASSWORD=<valid-demo-app-password>
APK_PATH=apps/mda-2.2.0-25.apk

APPIUM_HOST=127.0.0.1
APPIUM_PORT=4723

DEVICE_NAME=Pixel_2
DEVICE_UDID=emulator-5554

GEMINI_API_KEY=<your-gemini-api-key>
```

### Environment Variables

| Variable | Description |
| --- | --- |
| `USERNAME` | Username used by the authentication tests |
| `PASSWORD` | Password used by the authentication tests |
| `APK_PATH` | Local path to the My Demo App APK |
| `APPIUM_HOST` | Appium server host; normally `127.0.0.1` |
| `APPIUM_PORT` | Appium server port; normally `4723` |
| `DEVICE_NAME` | Android emulator name |
| `DEVICE_UDID` | Android emulator device ID |
| `GEMINI_API_KEY` | Google Gemini API key used for AI failure analysis |

Do not commit `.env` or API keys to Git. The `.env` file is excluded through `.gitignore`.

## Application APK

The project uses Sauce Labs My Demo App for Android version 2.2.0 / build 25.

The APK is not committed to this repository. For local execution, place the APK at:

```text
apps/mda-2.2.0-25.apk
```

GitHub Actions downloads the APK automatically before running the tests.

# Running the Tests Locally

Start an Android emulator using the AVD configured in your local environment.

You can start the emulator with:

```bash
./scripts/start_emulator.sh
```

Start Appium:

```bash
./scripts/start_appium.sh
```

Or start the complete local test environment:

```bash
./scripts/start_test_environment.sh
```

Once the emulator and Appium are ready, run the tests with pytest.

Run a specific test file:

```bash
pytest tests/mobile/authentication/test_invalid_password.py
```

Run all mobile tests:

```bash
pytest tests/mobile/
```

Run tests using pytest markers, for example:

```bash
pytest -m smoke
```

```bash
pytest -m regression
```

```bash
pytest -m authentication
```

Run emulator, start appium, and run tests using pytest:

```bash
./run_tests.sh <marker>
```

To generate Allure results:

```bash
pytest tests/mobile/ --alluredir=test-reports/allure-results
```

# Allure Reporting

Allure is used to provide a visual test report containing test metadata, steps, screenshots, and AI failure analysis.

Generate the HTML report:

```bash
allure generate test-reports/allure-results \
    -o test-reports/allure-report \
    --clean
```

Open the report locally:

```bash
allure open test-reports/allure-report
```

Failed tests can include:

* Failure screenshots
* Stack traces
* Allure test metadata
* Sanitized Android UI hierarchy
* AI Failure Analysis from Gemini

# GitHub Actions

The project includes a GitHub Actions workflow for automated Android test execution.

The workflow runs against an Android API 30 Pixel 2 emulator using x86_64 architecture and KVM hardware acceleration.

The workflow supports the following suites:

* `all`
* `smoke`
* `regression`
* `critical`
* `authentication`
* `cart`

Pushes default to the smoke suite, while the scheduled workflow runs the regression suite.

The workflow also:

* Installs Python dependencies
* Downloads the application APK
* Creates the Android emulator
* Starts Appium and the test environment
* Runs the selected pytest suite
* Collects Android diagnostics
* Generates an Allure HTML report
* Publishes the Allure report to GitHub Pages

The Gemini API key is provided to CI through the GitHub Actions `GEMINI_API_KEY` secret. The username is provided through a repository variable and the password through a repository secret.

# Test Coverage

The current tests include application launch, authentication, and cart scenarios.

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

This test currently demonstrates the AI failure-analysis capability by analyzing a known application behavior issue and explaining the failure using the functional test context and technical evidence.

## Cart

The cart tests cover cart behavior for both logged-in and logged-out users, including adding single and multiple items, changing quantities, removing items, and validating cart quantity behavior.

# Failure Screenshots

The framework automatically captures a screenshot when a test fails or is marked as an expected failure.

The screenshot is:

* Saved to the test reports directory.
* Attached to the corresponding Allure test result.

Screenshot handling is implemented in the pytest test lifecycle rather than inside page objects.

# Test Environment Configuration

Environment-specific values are kept outside the test code.

The project uses environment variables and `python-dotenv` for local configuration.

Sensitive values such as passwords and API keys are not stored in the Git repository.

The `.env` file is excluded through `.gitignore`.

# Application Under Test

This framework uses the Sauce Labs My Demo App for Android as the application under test.

The application provides a simple mobile shopping experience that is useful for demonstrating common mobile automation scenarios such as:

* Application launch
* Login
* Authentication errors
* Navigation
* Product interaction
* Shopping cart behavior

The application is used only as a test application for this portfolio project.

# Current Status

The framework currently supports Android UI automation using Appium, pytest, Allure, GitHub Actions, and Gemini-powered failure analysis.

## Completed

* Android emulator setup
* Appium server setup
* Appium driver configuration
* Page Object Model
* Locator layer
* Reusable BasePage
* Login, menu/header, catalog, product, and cart page models
* Authentication test scenarios
* Cart test scenarios for logged-in and logged-out users
* Device and application launch test
* External test data files
* Explicit waits
* Allure reporting
* Allure test metadata
* Failure screenshots
* Android UI hierarchy sanitization
* Structured FailureContext model
* Gemini AI failure analysis
* Test environment startup scripts
* GitHub Actions CI execution
* Allure report deployment to GitHub Pages

## Planned Improvements

* Add more mobile test scenarios
* Expand the page model and locator layers as new screens are tested
* Add additional API or data validation where appropriate
* Continue improving AI-assisted failure analysis as more failure types are covered
* Expand CI diagnostics and reporting as the framework grows

# Author

Jose Magtanong

QA Automation Engineer / SDET Portfolio Project
