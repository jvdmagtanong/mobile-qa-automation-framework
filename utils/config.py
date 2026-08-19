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
