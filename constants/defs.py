import os
from dotenv import load_dotenv
load_dotenv("../.env")

API_ID = os.environ.get("API_ID")
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
OPENFX_URL = os.environ.get("OPENFX_URL")

SECURE_HEADER = {
    "Authorization": f"Basic {API_ID}:{API_KEY}:{API_SECRET}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

LABEL_MAP = {
    'Open': 'o',
    'High': 'h',
    'Low': 'l',
    'Close': 'c',
}

THROTTLE_TIME = 0.3
