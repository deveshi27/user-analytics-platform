import os
import json
import requests
from requests.auth import HTTPBasicAuth

ES_HOST = os.getenv("ELASTIC_HOST")
ES_USER = os.getenv("ELASTIC_USERNAME")
ES_PASS = os.getenv("ELASTIC_PASSWORD")

def write_to_es(index_name, records):
    """
    records: list[dict]
    """
    if not records:
        return

    bulk_payload = ""
    for record in records:
        bulk_payload += json.dumps({"index": {"_index": index_name}}) + "\n"
        bulk_payload += json.dumps(record,default=str) + "\n"

    url = f"{ES_HOST}/_bulk"
    headers = {"Content-Type": "application/x-ndjson"}

    response = requests.post(
        url,
        data=bulk_payload,
        headers=headers,
        auth=HTTPBasicAuth(ES_USER, ES_PASS),
        timeout=30

    )

    if response.status_code >= 300:
        raise Exception(f"ES bulk insert failed: {response.text}")
