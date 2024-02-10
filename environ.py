import requests
import os

SECRET = os.getenv("SECRET")
res = requests.get(SECRET).json()
api_id = res["key"]["api_id"]
api_hash = res["key"]["api_hash"]
bot_token = res["bot"]["ai_tg"]
google_api = res["key"]["google_ai"]