import requests
import os

SECRET = os.getenv("SECRET")
TELECAST = os.getenv("TELECAST")
res = requests.get(SECRET).json()
google_api = res["key"]["google_ai"]
session = requests.get(TELECAST).text
