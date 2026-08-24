import json, pytest, re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "tests" / "data"


def read_json_file(file_name):
    data_file = DATA_DIR / f"{file_name}.json"

    with open(data_file, "r") as file:
        return json.load(file)


def get_pytest_param(file_name):
    test_data = read_json_file(file_name)
    return [pytest.param(data, id=create_test_id(data)) for data in test_data["data"]]


def create_test_id(data):
    if isinstance(data, dict):
        value = data["item_name"]
    else:
        value = data
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
