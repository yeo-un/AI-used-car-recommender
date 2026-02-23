import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("E_BASE_URL")

HEADERS = {
    "referer": os.getenv("E_REFERER"),
    "origin": os.getenv("E_ORIGIN"),
    "user-agent": os.getenv("E_USER_AGENT"),
}


def fetch_cars(cursor=""):

    params = {
        "count": "true",
        "cursor": cursor,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    data = fetch_cars()
    print(data)
