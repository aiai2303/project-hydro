from environment import api_id, api_hash, bot_token
from hydrogram import Client
import os

app = Client("Google AI", api_id, api_hash, bot_token=bot_token, plugins=dict(root='plugins'))

app.run()