import os
from dotenv import load_dotenv


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


USERNAME = get_required_env("USERNAME")
PASSWORD = get_required_env("PASSWORD")
APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = os.getenv("APPIUM_PORT", "4723")
DEVICE_NAME = os.getenv("DEVICE_NAME", "Pixel_10")
DEVICE_UDID = os.getenv("DEVICE_UDID", "emulator-5554")
APK_PATH = get_required_env("APK_PATH")