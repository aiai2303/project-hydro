from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from easygoogletranslate import EasyGoogleTranslate
from langdetect import detect
from io import BytesIO
import requests
import random

translator = EasyGoogleTranslate(
    source_language='vi',
    target_language='en',
    timeout=30
)

def diff(query):
    response = requests.get("https://diffusion.cloudlapse.workers.dev/", params=dict(q=query))
    return response
    
def polli(query):
    response = requests.get("https://image.pollinations.ai/prompt/" + query)
    return response

@Client.on_message(filters.command("image") & filters.incoming)
def image_generator(c, m):
    model = random.choice([diff, polli])
    if len(m.command) > 1:
        m.reply_chat_action(ChatAction.TYPING)
        query = m.text.split(m.command[0])[1]
        if detect(query) != "en":
            query = translator.translate(query)
        response = model(query)
        m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        if m.from_user:
            name = m.from_user.first_name
        else:
            name = "Channel/Group"
        if response.status_code == 200:
            result = BytesIO(response.content)
            result.name = "image.png"
            m.reply_photo(result, caption=f"By __**{name}**__", quote=True)