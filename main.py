from hydrogram import Client, filters
from environ import api_id, api_hash, bot_token
from hydrogram.enums import ChatAction
from res import pro, pro_vision
import os

app = Client("Google AI", api_id, api_hash, bot_token=bot_token, in_memory=True)

@app.on_message(filters.command(["start","help"]) & filters.private)
async def basic(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply("Hello, __--Welcome to Unofficial Google AI--__", quote=True)
    
@app.on_message((filters.mentioned | filters.private) & filters.text)
async def pro_model(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    if m.text.startswith("@"):
        text = m.text.split(m.command[0])
    else:
        text = m.text
    res = pro(text)
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply(res, quote=True)
    
def photo_message(_, __, m):
    return m.reply_to_message and m.reply_to_message.photo
    
@app.on_message((filters.mentioned | filters.private) & (filters.photo | filters.create(photo_message)))
async def pro_vision_model(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        if m.reply_to_message:
            text = m.text
            photo = await c.download_media(m.reply_to_message, in_memory=True)
        else:
            raise
    except Exception as e:
        print(e)
        text = m.caption
        photo = await c.download_media(m, in_memory=True)
    if text.startswith("@"):
        text = text.split(" ", 1)[1]
    res = pro_vision(photo, text)
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply(res, quote=True)
    
app.run()