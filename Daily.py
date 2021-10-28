import aiohttp
import asyncio
from datetime import datetime, timedelta
from api import WebApi, WebApiRequestError
from run import extract_csrf

if not hasattr(asyncio, 'create_task'):
    asyncio.create_task = asyncio.ensure_future

if not hasattr(asyncio, 'get_running_loop'):
    asyncio.get_running_loop = asyncio.get_event_loop


class Live:
    def __init__(self, uid, cookie, ruid, sendkey=None):
        self.uid = uid
        self.headers = {
            'Referer': 'https://live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36',
            'Cookie': cookie,
        }
        self.ruid = ruid
        self.csrf = extract_csrf(cookie)
        self.sendkey = sendkey
        self.message = ''

    async def run(self):
        self.session = session = aiohttp.ClientSession(headers=self.headers)
        try:
            self.room_id = (await WebApi.get_room_id(session, self.ruid))['roomid']
            hearts = [g for g in (await WebApi.get_gift(session)) if (g['gift_name'] == "小心心")]
            if not hearts:
                self.message += "在背包里未发现小心心"
                raise Exception(self.message)
            try:
                sign = await WebApi.do_sign(session)
                self.message += f"直播区签到成功(本月签到天数：{sign['hadSignDays']}/{sign['allDays']}\n"
            except WebApiRequestError:
                pass
            await WebApi.send_msg(session, self.room_id, self.csrf)
            self.message += "弹幕打卡成功\n"
            await WebApi.send_gifts(session, uid=self.uid, bag_id=hearts[0]['bag_id'],
                                    gift_id=hearts[0]['gift_id'], gift_num=hearts[0]['gift_num'],
                                    ruid=self.ruid, room_id=self.room_id, csrf=self.csrf)
            self.message += f"{hearts[0]['gift_num']}个小心心赠送成功\n"
            await asyncio.sleep(10)
            medal = [m for m in (await WebApi.get_fans_medal(session)) if self.room_id == m['room_id']][0]
            now = datetime.now()
            now += timedelta(days=(medal['next_intimacy'] -
                                   medal['intimacy']) // medal['today_feed'] + 1)
            medal_msg = f"目前：{medal['medal_name']}{medal['level']}级\n今日亲密度：{medal['today_feed']}/{medal['day_limit']}\n当前等级上限：{medal['intimacy']}/{medal['next_intimacy']}\n还需要{(medal['next_intimacy'] - medal['intimacy']) // 1300 + 1}天（{now.strftime('%m.%d')}）到达{medal['level'] + 1}级 "
            self.message += medal_msg
        except Exception as e:
            self.message += f"自动打卡出错：{repr(e)}"
        await WebApi.secret_player(session, self.csrf)
        await session.close()
        if self.sendkey:
            await self.ServerChan()
            print("Server酱已推送")

    async def ServerChan(self):
        url = f'https://sctapi.ftqq.com/{self.sendkey}.send'
        data = {
            'title': '直播间打卡推送',
            'desp': self.message.replace('\n', '\n\n')
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data) as resp:
                return await resp.json()
