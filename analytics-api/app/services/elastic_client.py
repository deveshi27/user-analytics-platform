import time
import requests
from requests.auth import HTTPBasicAuth

from app.core.config import (
    ELASTIC_HOST,
    ELASTIC_USERNAME,
    ELASTIC_PASSWORD,
)

HEADERS = {
    "Content-Type": "application/json"
}

def search(index: str, query: dict, retries: int = 5):
    url = f"{ELASTIC_HOST}/{index}/_search"

    for attempt in range(retries):
        try:
            response = requests.post(
                url=url,
                headers=HEADERS,
                auth=HTTPBasicAuth(
                    ELASTIC_USERNAME,
                    ELASTIC_PASSWORD
                ),
                json=query,
                timeout=10
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as exc:
            if attempt == retries - 1:
                raise exc
            time.sleep(2)