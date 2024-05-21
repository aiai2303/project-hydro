import requests
import os

SECRET = os.getenv("SECRET")
res = requests.get(SECRET).json()
google_api = res["key"]["google_ai"]

neon_url = res["data"]["neon"]

api_id = res["key"]["api_id"]

api_hash = res["key"]["api_hash"]

bot_token = res["bot"]["ai_tg"]
