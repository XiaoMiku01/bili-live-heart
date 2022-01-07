import asyncio
import json
import sys
import time
from run import main
from Daily import Live
from bili.login import BiliUser
from bili.smallheart import SmallHeartTask
from bili.dailyclockin import DailyClockIn


def main_handler(event, context):
    print("start!")
    data = json.loads(context["environment"])
    uid, cookie = data["uid"], data["cookie"]
    ruid = data.get("ruid", None)
    sendkey = data.get("sendkey", None)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(uid, cookie, cloud_service=True))
    except Exception as e:
        print(f"运行出错:{repr(e)}")
        return False
    time.sleep(10)
    l = Live(uid, cookie, ruid, sendkey)
    loop.run_until_complete(l.run())
    print(l.message)
    print("complete!")
    return True


if __name__ == "__main__":
    import toml

    config = toml.load("user.toml")["user"]
    cookie = config["cookie"]
    ruid = config["ruid"]
    sendkey = config["sendkey"]
    user = BiliUser(cookie, ruid, sendkey)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(user.login())
    loop.run_until_complete(SmallHeartTask(user).do_work())
    loop.run_until_complete(DailyClockIn(user).do_work())
    loop.run_until_complete(user.session.close())
    print(user.message)
    print(user.message_err)