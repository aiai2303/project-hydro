import os
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from hydrogram.enums import ChatAction
from plugins.ranking.model import DB
from plugins.dice.util import prettier
from plugins.dice.model import Database, Model64


def schedule(c):
    def dice_rank():
        c.send_chat_action("share_v2ray_file", ChatAction.TYPING)
        db = Database()
        result_list = db.list(Model64)
        users = []
        for item in result_list:
            if item.last_name:
                name = item.first_name + " " + item.last_name
            else:
                name = item.first_name
            user = name
            point = item.point
            users.append((user, point))
        ranks = prettier(users)
        text = [
            "<b>Vòng Quay Vận Mệnh</b>",
            "\n\n".join(ranks),
            "__Ném `🎰` để tham gia Vòng Quay Vận Mệnh__",
        ]
        text = "\n\n\n".join(text)
        msg = c.send_message("share_v2ray_file", text)
        if os.getenv("PRE_MESSAGE_ID"):
            msg_id = os.getenv("PRE_MESSAGE_ID")
            try:
                c.delete_messages("share_v2ray_file", int(msg_id))
            except:
                pass
        os.environ["PRE_MESSAGE_ID"] = str(msg.id)

    def reset_rank():
        db = DB()
        db.reset_daily()
        db = Database()
        db.reset()

    def new_day():
        c.send_chat_action("share_v2ray_file", ChatAction.TYPING)
        c.send_message(
            "share_v2ray_file", "Ngày mới bắt đầu, hãy ném `🎰` để xác định vận mệnh..."
        )

    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")

    scheduler = BackgroundScheduler()

    scheduler.add_job(dice_rank, "interval", minutes=30)

    scheduler.add_job(reset_rank, CronTrigger(hour=0, minute=0, timezone=vietnam_tz))

    scheduler.add_job(new_day, CronTrigger(hour=5, minute=0, timezone=vietnam_tz))

    scheduler.start()
