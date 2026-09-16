from dataclasses import dataclass


@dataclass
class FailureContext:
    """Contains the information needed to analyze an automated test failure."""

    # Test metadata
    test_name: str
    epic: str | None = None
    feature: str | None = None
    story: str | None = None
    description: str | None = None

    # Failure evidence
    stack_trace: str | None = None
    page_source: str | None = None

    # Test environment
    framework: str = "Appium + Python + Pytest"
    device: str | None = None
    android_version: str | None = None
    appium_version: str | None = None

    