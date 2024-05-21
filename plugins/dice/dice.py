import random
import time
from datetime import datetime, timedelta
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import ChatPermissions
from .model import Database, Model64, Model6, Model5
from .util import prettier


def punish(m):
    mtime = random.randint(1, 1000)
    m.reply(
        f"**{m.from_user.first_name}** nhận được `{m.dice.value}` điểm, quá đen đủi cho ngày hôm nay. Hãy dành `{mtime}` phút cuộc đời để suy nghĩ về số phận.",
        quote=True,
    )
    now = datetime.now()
    delta = timedelta(minutes=mtime)
    targ = now + delta
    m.chat.restrict_member(
        m.from_user.id,
        ChatPermissions(can_send_messages=False),
        until_date=targ,
    )


def already(m, point):
    temp = m.reply(
        f"**{m.from_user.first_name}**, hôm nay bạn đã thử vận may với cái này rồi, không thể thực hiện lại nữa, hãy chờ ngày mai hoặc thử cái khác.\n\nĐiểm của bạn là  **{point}**",
        quote=True,
    )
    m.delete()
    time.sleep(10)
    temp.delete()


def update(m, db, model):
    db.update(
        m.from_user.id,
        m.from_user.first_name,
        m.from_user.last_name,
        m.from_user.username,
        m.dice.value,
        model,
    )


@Client.on_message(filters.dice)
def roll_dice(c, m):
    db = Database()
    m.reply_chat_action(ChatAction.TYPING)
    dice = m.dice
    if dice.emoji == "🎰":
        user = db.get(m.from_user.id, Model64)
        if user:
            return already(m, user.point)
        update(m, db, Model64)

        if dice.value > 59:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm. Hôm nay bạn thật may mắn🎉",
                quote=True,
            )
        elif dice.value > 19:
            m.reply(
                f"**{m.from_user.first_name}** nhận được `{dice.value}` điểm.",
                quote=True,
            )
        else:
            punish(m)
    elif dice.emoji in ["🎳", "🎯", "🎲"]:
        user = db.get(m.from_user.id, Model6)
        if user:
            return already(m, user.point)
        update(m, db, Model6)

        if dice.value == 6:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm. Hôm nay bạn thật may mắn🎉",
                quote=True,
            )
        elif dice.value > 2:
            m.reply(
                f"**{m.from_user.first_name}** nhận được `{dice.value}` điểm.",
                quote=True,
            )
        else:
            punish(m)
    else:
        user = db.get(m.from_user.id, Model5)
        if user:
            return already(m, user.point)
        update(m, db, Model5)

        if dice.value == 5:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm. Hôm nay bạn thật may mắn🎉",
                quote=True,
            )
        elif dice.value > 1:
            m.reply(
                f"**{m.from_user.first_name}** nhận được `{dice.value}` điểm.",
                quote=True,
            )
        else:
            punish(m)


@Client.on_message(filters.command("dice"))
def get_dice_rank(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = Database()
    rows = db.list(Model64)
    users = []
    for row in rows:
        if row.last_name:
            name = row.first_name + " " + row.last_name
        else:
            name = row.first_name
        point = row.point
        users.append((name, point))
    ranks = prettier(users)
    text = [
        "<b>Bảng xếp hạng __Vòng Quay Vận Mệnh__</b>",
        "\n\n".join(ranks),
        "__Ném `🎰` để tham gia nền văn minh này__",
    ]
    text = "\n\n\n".join(text)
    m.reply(text, quote=True)
