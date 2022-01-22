import logging
import asyncio
import time
import datetime
import pytz
import calendar
from collections import namedtuple
from asyncio import CancelledError

from .api import WebApi, medals, get_info, WebApiRequestError
from .login import BiliUser

if not hasattr(asyncio, "create_task"):
    asyncio.create_task = asyncio.ensure_future


RoomInfo = namedtuple("RoomInfo", "room_id, parent_area_id, area_id, owner, ruid")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("smallheart")


def get_beijing_0():
    local_format = "%Y-%m-%d %H:%M:%S"
    beijing_tz = pytz.timezone("Asia/Shanghai")
    time_str = time.strftime(local_format, time.localtime(int(time.time())))
    dt = datetime.datetime.strptime(time_str, local_format)
    utc_dt = dt.astimezone(beijing_tz)
    utc_0 = calendar.timegm(utc_dt.timetuple())
    beijing_0 = utc_0 - (utc_0 % (24 * 3600)) - 8 * 3600
    return beijing_0


class SmallHeartTask:
    def __init__(self, user: BiliUser):
        self.user = user
        self.MAX_HEARTS_PER_DAY = 24
        self.MAX_CONCURRENT_ROOMS = self.MAX_HEARTS_PER_DAY
        self.HEART_INTERVAL = 300

    async def hearts_num_send(self, session, ruid=None):
        result = await WebApi.gifts_record(session)
        num = 0
        ruid_temp = ruid
        beijing_0 = get_beijing_0()
        for i in result["list"]:
            if ruid_temp == None:
                ruid = i["ruid"]
            if (i["gift_name"] == "小心心" and beijing_0 < i["timestamp"] < time.time() and i["ruid"] == ruid):
                num += i["gift_num"]
                rname = i["r_uname"]
        if num >= self.MAX_HEARTS_PER_DAY and ruid_temp:
            logger.info(f'今天已经给{rname}({i["ruid"]})送过{num}个小心心了')
        elif 0 < num < self.MAX_HEARTS_PER_DAY and ruid_temp:
            logger.info(
                f'今天已经给{rname}({i["ruid"]})送过{num}个小心心了,还差{self.MAX_HEARTS_PER_DAY-num}个'
            )
        return num

    async def get_hearts_7_days(self, session):
        hearts_7_days = [
            h
            for h in (await WebApi.get_gift(session))
            if h["gift_name"] == "小心心" and h["corner_mark"] == "7天"
        ]
        if len(hearts_7_days):
            logger.info(
                f"今日以获取{hearts_7_days[0]['gift_num']}个小心心,剩余{self.MAX_HEARTS_PER_DAY-hearts_7_days[0]['gift_num']}个"
            )
            return hearts_7_days[0]["gift_num"]
        return 0

    async def send_gifts(self, session):
        if self.user.ruid:
            logger.info("开始赠送小心心")
            try:
                self.user.room_info = []
                async for m in medals(session):
                    try:
                        info = await get_info(session, m["roomid"])
                    except KeyError:
                        continue
                    room_id = info["room_id"]
                    area_id = info["area_id"]
                    parent_area_id = info["parent_area_id"]
                    owner = m["uname"]
                    ruid = m["target_id"]
                    room_info = RoomInfo(room_id, parent_area_id, area_id, owner, ruid)
                    if m["target_id"] == self.user.ruid:
                        self.user.medal_id = m["medal_id"]
                    self.user.room_info.append(room_info)
                rroomd_id, _, _, owner, ruid = [
                    r for r in self.user.room_info if r.ruid == self.user.ruid
                ][0]
                gifts = [g for g in (await WebApi.get_gift(session))]
                hearts_num_send = await self.hearts_num_send(session, self.user.ruid)
                if gifts:
                    for g in gifts:
                        if g["gift_name"] not in ["小心心", "辣条"]:
                            continue
                        if (
                            g["gift_name"] == "小心心"
                            and hearts_num_send + g["gift_num"] < 30
                        ):
                            hearts_num_send += g["gift_num"]
                        elif (
                            g["gift_name"] == "小心心"
                            and hearts_num_send + g["gift_num"] >= 30
                        ):
                            g["gift_num"] = 30 - hearts_num_send
                            hearts_num_send = 30
                            if g["gift_num"] <= 0:
                                continue
                        try:
                            await WebApi.send_gifts(
                                session=session,
                                uid=self.user.uid,
                                bag_id=g["bag_id"],
                                gift_id=g["gift_id"],
                                gift_num=g["gift_num"],
                                ruid=ruid,
                                room_id=rroomd_id,
                                csrf=self.user.csrf,
                            )
                            message = f"赠送{owner}(UID:{ruid} 房间号:{rroomd_id}){g['gift_name']}x{g['gift_num']}成功"
                            logger.info(message)
                            self.user.message.append(message)
                            await asyncio.sleep(2)
                        except WebApiRequestError as e:
                            logger.error(e)
                            self.user.message_err.append(e)
                            continue
                else:
                    message_err = "背包里未发现小心心"
                    logger.error(message_err)
                    self.user.message_err.append(message_err)
            except IndexError:
                message_err = "未找到目标房间信息,请检查输入的房主UID(不是房间号)是否正确"
                logger.error(message_err)
                self.user.message_err.append(message_err)
                return
        else:
            message = "未设置赠送目标UID"
            logger.info(message)
            self.user.message.append(message)

    async def do_work(self, HEART_NUM=None):
        logger.info(f"开始小心心任务")
        self.session = session = self.user.session
        MAX_HEARTS_PER_DAY = self.MAX_HEARTS_PER_DAY - (
            await self.get_hearts_7_days(session) + await self.hearts_num_send(session)
        )

        if HEART_NUM:
            MAX_HEARTS_PER_DAY = HEART_NUM
        try:
            if self.user.room_info == []:
                room_infos = []
                count = 0
                async for m in medals(session):
                    try:
                        info = await get_info(session, m["roomid"])
                    except KeyError:
                        continue
                    room_id = info["room_id"]
                    area_id = info["area_id"]
                    parent_area_id = info["parent_area_id"]
                    owner = m["uname"]
                    ruid = m["target_id"]
                    room_info = RoomInfo(room_id, parent_area_id, area_id, owner, ruid)

                    if parent_area_id == 0 or area_id == 0:
                        continue
                    room_infos.append(room_info)
                    count += 1
                    if count == MAX_HEARTS_PER_DAY:
                        break
                self.user.room_info = room_infos
            else:
                room_infos = self.user.room_info
            if len(room_infos) == 0:
                raise Exception(f"一个粉丝牌都没有~结束任务")
            self.queue = queue = asyncio.Queue(MAX_HEARTS_PER_DAY)

            for i in range(1, MAX_HEARTS_PER_DAY + 1):
                queue.put_nowait(i)
            await self.dispatch(room_infos)
            await queue.join()
        except CancelledError:
            raise
        finally:
            try:
                for task in self.tasks:
                    task.cancel()
            except Exception:
                pass
        logger.info(f"小心心任务已完成")
        await asyncio.sleep(10)
        remaining = self.MAX_HEARTS_PER_DAY - (
            await self.get_hearts_7_days(session) + await self.hearts_num_send(session)
        )
        if remaining > 0:
            await self.do_work(remaining)
            return
        await self.send_gifts(session)

    async def dispatch(self, room_infos):
        self.tasks = tasks = []
        for room_info in room_infos:

            task = asyncio.create_task(self.post_heartbeats(*room_info))
            tasks.append(task)

    async def post_heartbeats(self, room_id, parent_area_id, area_id, owner, *others):
        session = self.session
        csrf = self.user.csrf
        buvid = self.user.buvid
        uuid = self.user.uuid
        queue = self.queue

        while True:
            sequence = 0

            try:
                result = await WebApi.post_enter_room_heartbeat(
                    session, csrf, buvid, uuid, room_id, parent_area_id, area_id
                )
                logger.info(
                    f'进入{owner}({room_id})直播间心跳已发送,{result["heartbeat_interval"]}秒后发送第一个心跳'
                )
                while True:
                    sequence += 1
                    interval = result["heartbeat_interval"]
                    await asyncio.sleep(interval)

                    result = await WebApi.post_in_room_heartbeat(
                        session,
                        csrf,
                        buvid,
                        uuid,
                        room_id,
                        parent_area_id,
                        area_id,
                        sequence,
                        interval,
                        result["timestamp"],
                        result["secret_key"],
                        result["secret_rule"],
                    )

                    logger.info(f"{owner}({room_id})直播间内第{sequence}个心跳已发送")
                    assert self.HEART_INTERVAL % interval == 0, interval
                    heartbeats_per_heart = self.HEART_INTERVAL // interval

                    if sequence % heartbeats_per_heart == 0:
                        n = queue.get_nowait()
                        logger.info(f"获得第{n}个小心心")
                        queue.task_done()
            except asyncio.QueueEmpty:
                logger.info(f"小心心任务已完成, {owner}({room_id})直播间心跳任务终止")
                break
            except CancelledError:
                raise
            except Exception as e:
                if sequence == 0:
                    logger.error(f"进入{owner}({room_id})直播间心跳发送异常: {repr(e)}")
                else:
                    logger.error(f"{owner}({room_id})直播间内第{sequence}个心跳发送异常: {repr(e)}")

                delay = 60
                logger.warning(f"{delay}秒后重试{owner}({room_id})直播间心跳任务")
                await asyncio.sleep(delay)
