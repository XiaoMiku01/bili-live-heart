import os
import json
import asyncio

from bili.login import BiliUser
from bili.smallheart import SmallHeartTask
from bili.dailyclockin import DailyClockIn
from push import serverchan

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


def get_config():
    try:
        with open("./local_config.json", "r") as f:
            config = json.loads(f.read())
    except:
        config = json.loads(os.getenv("config"))
    return config


def main():
    config = get_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sendkey = config["sendkey"]
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


if __name__ == "__main__":
    main()
