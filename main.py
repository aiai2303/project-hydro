from hydrogram import Client, filters
from environ import api_id, api_hash, bot_token, google_api
from preset import generation_config, safety_settings
from hydrogram.enums import ChatAction
import google.generativeai as genai
import os

app = Client("Google AI", api_id, api_hash, bot_token=bot_token)
genai.configure(api_key=google_api)
model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)
convo = model.start_chat(history=[
])

@app.on_message(filters.command(["start","help"]) & filters.private)
async def basic(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply("Hello, __--Welcome to Unofficial Google AI--__", quote=True)
    
@app.on_message(filters.mentioned | filters.private)
async def chatting(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    convo.send_message(m.text)
    res = convo.last.text
    await m.reply(res, quote=True)
    
app.run()