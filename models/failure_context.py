
class FailureContext:
    """
    A class to hold the context of a test failure, including the test name, error message, and any additional
    information that may be useful for debugging.
    """

    def __init__(self, test_name,
                        story=None,
                        scenario=None,
                        steps=None,
                        expected_result=None,
                        stack_trace=None,
                        page_source=None,
                        framework="Appium + Python + Pytest",
                        device=None,
                        android_version=None,
                        appium_version=None):
        self.test_name = test_name
        self.story = story
        self.scenario = scenario
        self.steps = steps
        self.expected_result = expected_result
        self.stack_trace = stack_trace
        self.page_source = page_source
        self.framework = framework
        self.device = device
        self.android_version = android_version
        self.appium_version = appium_version
