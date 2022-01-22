import asyncio
import logging
from datetime import datetime, timedelta
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
            await asyncio.sleep(6)
        self.user.message.append(
            f"弹幕打卡成功: {len(self.user.room_info) - err_num}/{len(self.user.room_info)}"
        )
        if self.user.ruid:
            medal_0 = (await WebApi.get_weared_medal(self.user.session, self.user.csrf))
            if medal_0:
                medal_0_id = medal_0['medal_id']
            await asyncio.sleep(1)
            await WebApi.wear_medal(
                self.user.session, self.user.medal_id, self.user.csrf
            )  # wear medal
            medal = await WebApi.get_weared_medal(self.user.session, self.user.csrf)
            now = datetime.now()
            now += timedelta(
                days=(medal["next_intimacy"] - medal["intimacy"]) // medal["today_feed"]
                + 1
            )
            message = f"目前：{medal['medal_name']}{medal['level']}级\n今日亲密度：{medal['today_feed']}/{medal['day_limit']}\n当前等级上限：{medal['intimacy']}/{medal['next_intimacy']}\n预计还需要{(medal['next_intimacy'] - medal['intimacy']) // medal['today_feed'] + 1}天（{now.strftime('%m.%d')}）到达{medal['level'] + 1}级 "
            self.user.message.append(message)
            if medal_0:
                await asyncio.sleep(1)
                await WebApi.wear_medal(
                    self.user.session, medal_0_id, self.user.csrf
                )
