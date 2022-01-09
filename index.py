import asyncio
import json
import datetime
from bili.login import BiliUser
from bili.smallheart import SmallHeartTask
from bili.dailyclockin import DailyClockIn
from push import serverchan, ifttt_telegram

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


async def run(user: BiliUser):
    await user.login()
    await SmallHeartTask(user).do_work()
    await DailyClockIn(user).do_work()
    await user.session.close()
    message = f"用户:{user.uname}({user.uid})\n" + "\n".join(user.message)
    if user.message_err:
        message += "\n错误日志:\n" + "\n".join(user.message_err)
    return message + "\n\n"


def main_handler(event, context):
    data = json.loads(context["environment"])
    cookie = data["cookie"]
    ruid = int(data.get("ruid", 0))
    sendkey = data.get("sendkey", None)
    ifttt_event_name = data.get("ifttt_telegram_event_name", None)
    ifttt_key = data.get("ifttt_telegram_key", None)
    loop = asyncio.get_event_loop()
    message = ""
    try:
        user = BiliUser(cookie=cookie, ruid=ruid, cloud_service=True)
        message = loop.run_until_complete(run(user))
    except Exception as e:
        message = str(e)
    print(message)
    if sendkey:
        loop.run_until_complete(serverchan.push_message(sendkey, message))
    if ifttt_event_name and ifttt_key:
        loop.run_until_complete(ifttt_telegram.push_message(ifttt_event_name, ifttt_key, message))
    return True


def main():
    import toml

    config = toml.load("user.toml")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sendkey = config["serverchan"]["sendkey"]
    ifttt_event_name = config["ifttt_telegram"]["event_name"]
    ifttt_key = config["ifttt_telegram"]["key"]
    message = ""
    for u in config["users"]:
        if u["cookie"] == "":
            continue
        try:
            user = BiliUser(u["cookie"], u["ruid"])
            message += loop.run_until_complete(run(user))
        except Exception as e:
            message += f"{e}\n"
    print(message)
    if sendkey:
        loop.run_until_complete(serverchan.push_message(sendkey, message))
    if ifttt_event_name and ifttt_key:
        loop.run_until_complete(ifttt_telegram.push_message(ifttt_event_name, ifttt_key, message))


if __name__ == "__main__":
    cron = "0 0 */1 * *"
    schedulers = BlockingScheduler()
    schedulers.add_job(
        main,
        CronTrigger.from_crontab(cron),
        id="main",
        next_run_time=datetime.datetime.now(),
    )
    schedulers.start()
