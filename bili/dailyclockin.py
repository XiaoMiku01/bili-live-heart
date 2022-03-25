import asyncio
import logging
from datetime import datetime, timedelta
from .login import BiliUser
from .api import WebApi, medals, get_info, WebApiRequestError


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
        try:
            rooms = []
            async for m in medals(self.user.session):
                rooms.append(m)
                try:
                    info = await get_info(self.user.session, m["roomid"])
                except KeyError:
                    continue
                try:
                    await WebApi.send_msg(self.user.session, info["room_id"], self.user.csrf)
                    logger.info(f"{m['uname']}({m['target_id']})直播间打卡成功")
                except Exception as e:
                    message_err = f"{m['uname']}({m['target_id']})直播间打卡失败: {e}"
                    logger.error(message_err)
                    self.user.message_err.append(message_err)
                    err_num += 1
                await asyncio.sleep(6)
        except Exception as e:
            logger.error(e)
            self.user.message_err.append(e)
            err_num += 1
        self.user.message.append(
            f"弹幕打卡成功: {len(rooms) - err_num}/{len(rooms)}"
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

            if medal["today_feed"] == 0 and medal['level'] > 20:
                self.user.message_err.append(f"{medal['medal_name']}{medal['level']}级大于20级，打卡不加亲密度，只会点亮牌子")
                return
            if medal["today_feed"] == 0:
                self.user.message_err.append(f"你设置的主播亲密度获取失败")
                return
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
