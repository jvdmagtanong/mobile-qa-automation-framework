import os

from google import genai


def analyze_test_failure(
    test_name,
    story=None,
    scenario=None,
    steps=None,
    expected_result=None,
    stack_trace=None,
    page_source=None,
    framework="Appium + Python + Pytest",
    device=None,
    android_version=None,
    appium_version=None,
):
    """
    Sends a mobile test failure to Gemini for automated root-cause analysis.

    The analyzer receives the test's functional context together with the
    technical failure details so Gemini can distinguish application defects
    from automation, locator, synchronization, Appium, or environment issues.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API Key not found. Please set the GEMINI_API_KEY environment variable."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert SDET and mobile QA automation engineer.

Analyze the following automated mobile test failure. Use the functional test
context and technical evidence together. Do not assume that every failure is
a test automation problem or an application defect. Base your conclusion on
the evidence provided and clearly identify uncertainty when the evidence is
insufficient.

Test Name:
{test_name}

Test Story:
{story or "Not provided"}

Test Scenario:
{scenario or "Not provided"}

Test Steps:
{steps or "Not provided"}

Expected Result:
{expected_result or "Not provided"}

Framework:
{framework}

Device:
{device or "Not provided"}

Android Version:
{android_version or "Not provided"}

Appium Version:
{appium_version or "Not provided"}

Failure / Stack Trace:
{stack_trace or "Not provided"}
"""

    if page_source:
        prompt += f"""

Android Page Source at time of failure:
{page_source[:8000]}
"""

    prompt += """

Classify the most likely cause using one of these categories:
1. Application defect
2. Automation/test defect
3. Locator problem
4. Timing/synchronization issue
5. Appium/UiAutomator2 issue
6. Environment/device issue
7. Insufficient evidence

Provide your analysis in exactly this structure:

1. **Root Cause Summary**
A concise explanation of what most likely caused the failure.

2. **Failure Classification**
Choose one category from the list above and explain why.

3. **Evidence**
List the specific evidence from the test scenario, expected result, stack trace,
page source, or environment that supports the classification.

4. **Recommended Fix**
Give a practical recommendation. If a code change is appropriate, include a
small relevant code example. Do not recommend changing the test merely to make
it pass unless the evidence indicates the test is incorrect.

5. **Confidence Level**
State High, Medium, or Low and explain what additional evidence would increase
confidence if necessary.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Failed to generate analysis from Gemini: {str(e)}"
