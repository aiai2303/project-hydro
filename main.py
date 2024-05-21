from environment import api_id, api_hash, bot_token
from hydrogram import Client, idle
from schedule import schedule

app = Client(
    "Google AI", api_id, api_hash, bot_token=bot_token, plugins=dict(root="plugins")
)
app.start()
schedule(app)
idle()
