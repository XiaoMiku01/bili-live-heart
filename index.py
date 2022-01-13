import asyncio
import json
import datetime
from bili.login import BiliUser
from bili.smallheart import SmallHeartTask
from bili.dailyclockin import DailyClockIn
from push import pushaio
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
    push = eval(data["onepush"])
    loop = asyncio.get_event_loop()
    message = ""
    try:
        user = BiliUser(cookie=cookie, ruid=ruid, cloud_service=True)
        message += loop.run_until_complete(run(user))
    except Exception as e:
        message += str(e)
    print(message)
    if pushaio:
        pushaio.notify_me(push, f'【粉丝牌助手推送】', message.replace("\n", "\n\n"))
    return True


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    message = ""
    for u in config["users"]:
        if u["cookie"] == "":
            continue
        try:
            user = BiliUser(u["cookie"], u["ruid"])
            message += loop.run_until_complete(run(user))
        except Exception as e:
            message += f"{e}\n"
    push = eval(config['onepush'].get('onepush'))
    print(message)
    if pushaio:
        pushaio.notify_me(push, f'【粉丝牌助手推送】', message.replace("\n", "\n\n"))


if __name__ == "__main__":
    import toml

    config = toml.load("user.toml")
    cron = config["cron"]["cron"] if config["cron"]["cron"] else "0 0 * * *"
    schedulers = BlockingScheduler()
    schedulers.add_job(
        main,
        CronTrigger.from_crontab(cron),
        next_run_time=datetime.datetime.now(),
    )
    schedulers.start()
