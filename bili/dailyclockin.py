import asyncio
import logging
from .login import BiliUser
from .api import WebApi, WebApiRequestError


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("dailyclockin")


class DailyClockIn:
    def __init__(self, user: BiliUser):
        self.user = user

    async def do_work(self):
        logger.info("开始每日弹幕打卡任务")
        err_num = 0
        for room in self.user.room_info:
            try:
                await WebApi.send_msg(self.user.session, room.room_id, self.user.csrf)
                logger.info(f"{room.owner}({room.ruid})直播间打卡成功")
            except WebApiRequestError as e:
                message_err = f"{room.owner}({room.ruid})直播间打卡失败: {e}"
                logger.error(message_err)
                self.user.message_err.append(message_err)
                err_num += 1
            await asyncio.sleep(2)
        self.user.message.append(
            f"弹幕打卡成功: {len(self.user.room_info) - err_num}/{len(self.user.room_info)}"
        )
        await WebApi.secret_player(self.user.session, self.user.csrf)  # secret player
