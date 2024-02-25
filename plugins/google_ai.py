from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from res import pro, pro_vision, reset

@Client.on_message(filters.command("new"))
def refresh_chat(c, m):
    m.delete()
    reset()
    m.delete()
    
def photo_message(_, __, m):
    return m.reply_to_message and m.reply_to_message.photo
    
@Client.on_message((filters.mentioned | filters.private) & (filters.photo | filters.create(photo_message)) & filters.incoming)
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
    if not text:
        text = "Phân tích ảnh này"
    if text.startswith("@"):
        text = text.split(" ", 1)[1]
    try:
        res = pro_vision(photo, text)
        await m.reply_chat_action(ChatAction.TYPING)
        await m.reply(res, quote=True)
    except Exception as e:
        await m.reply(str(e), quote=True)
        
def _user_(_, __, m):
    return len(m.from_user.id) > 6
    
@Client.on_message((filters.mentioned | filters.private) & filters.text & filters.create(_user_) & filters.incoming)
async def pro_model(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    if m.text.startswith("@"):
        text = m.text.split(" ", 1)[1]
    else:
        text = m.text
    try:
        res = pro(text)
        await m.reply_chat_action(ChatAction.TYPING)
        await m.reply(res, quote=True)
    except Exception as e:
        await m.reply(str(e), quote=True)