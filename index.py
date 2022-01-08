import asyncio
import json
from bili.login import BiliUser
from bili.smallheart import SmallHeartTask
from bili.dailyclockin import DailyClockIn
from push import serverchan


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
    ruid = data.get("ruid", None)
    sendkey = data.get("sendkey", None)
    loop = asyncio.get_event_loop()
    message = ""
    try:
        user = BiliUser(cookie=cookie, ruid=ruid)
        message = loop.run_until_complete(run(user))
    except Exception as e:
        message = str(e)
    print(message)
    if sendkey:
        loop.run_until_complete(serverchan.push_message(sendkey, message))
    return True


if __name__ == "__main__":
    import toml

    config = toml.load("user.toml")
    loop = asyncio.get_event_loop()
    sendkey = config["serverchan"]["sendkey"]
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