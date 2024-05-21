from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from easygoogletranslate import EasyGoogleTranslate
from langdetect import detect
from io import BytesIO
import requests

translator = EasyGoogleTranslate(source_language="vi", target_language="en", timeout=30)


def diff(query):
    response = requests.get(
        "https://diffusion.cloudlapse.workers.dev/", params=dict(q=query)
    )
    return response


@Client.on_message(filters.command("image") & filters.incoming)
def image_generator(c, m):
    if len(m.command) > 1:
        m.reply_chat_action(ChatAction.TYPING)
        prompt = m.text.split(m.command[0])[1]
        if detect(prompt) != "en":
            query = translator.translate(prompt)
        else:
            query = prompt
        response = diff(query)
        m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        if m.from_user:
            name = m.from_user.first_name
        else:
            name = "Channel/Group"
        if response.status_code == 200:
            result = BytesIO(response.content)
            result.name = "image.png"
            m.reply_photo(result, caption=f"```{name}\n{prompt}```", quote=True)
