import os

ELASTIC_HOST = os.getenv("ELASTIC_HOST")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

API_KEY = os.getenv("ANALYTICS_API_KEY", "dev-key")
ES_INDEX = "user_metrics_silver"