import aiohttp
import asyncio
from datetime import datetime, timedelta
from api import WebApi, WebApiRequestError
from run import extract_csrf, medals, get_info

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
        self.err_message = ''
        self.total = [0, 0]     # 用于记录任务成功&出错数量，列表中第一个数字代表成功数量，第二个代表出错数量
        self.request = 0        # 用于请求获取小心心

    async def run(self):
        self.session = session = aiohttp.ClientSession(headers=self.headers)
        try:
            # 直播区签到
            self.room_id = (await WebApi.get_room_id(session, self.ruid))['live_room']['roomid'] if self.ruid else None
            print("\n开始直播区签到...")
            try:
                sign = await WebApi.do_sign(session)
                self.message += f"✔ 直播区签到成功(本月签到天数：{sign['hadSignDays']}/{sign['allDays']})\n"
                self.total[0] += 1
            except WebApiRequestError:
                self.message += "✔ 今日已签到过,无法重复签到\n"
                self.total[0] += 1
            print("Finish.\n")
            await asyncio.sleep(3)

            # 直播间打卡
            room_num = 0
            print("开始直播间打卡...\n")
            async for m in medals(session):
                if room_num > 99:
                    self.err_message += "✘ 打卡超过100个直播间，结束打卡\n"
                    self.total[1] += 1
                    break
                try:
                    info = await get_info(session, m['roomid'])
                except KeyError:
                    continue
                room_id = info['room_id']
                try:
                    await WebApi.send_msg(session, room_id, self.csrf)
                    print(m['target_name'], '房间{}已打卡'.format(room_id))
                    room_num += 1
                except Exception as e:
                    self.err_message += f'✘ 房间：{room_id}打卡失败:{repr(e)}\n'
                    self.total[1] += 1
                await asyncio.sleep(1)
            self.message += f"✔ {room_num}个房间打卡成功\n"
            self.total[0] += 1
            print("Finish.\n")
            await asyncio.sleep(3)
        except Exception as e:
            self.err_message += f"✘ 自动打卡出错：{repr(e)}"
            self.total[1] += 1
        await asyncio.sleep(3)
        # 我去，一个魂！
        try:
            await WebApi.secret_player(session, self.csrf)
            pass
        except Exception:
            pass
        await session.close()

    # 自动送礼物（逻辑顺序修改见自述文件）
    async def gift(self):
        print("开始礼物任务...\n")
        self.session = session = aiohttp.ClientSession(headers=self.headers)
        if self.ruid:
            if self.room_id:
                medal = [m for m in (await WebApi.get_fans_medal(session)) if self.room_id == m['room_id']][0]
                now = datetime.now()
                now += timedelta(days=(medal['next_intimacy'] -
                                       medal['intimacy']) // medal['today_feed'] + 1)
                if medal['today_feed'] < 1300:
                    gifts = [g for g in (await WebApi.get_gift(session))]
                    if gifts:
                        heart_num = 0
                        spicy_strips = 0
                        for g in gifts:
                            if g['gift_name'] == '小心心' and heart_num < 30:
                                gift_num = g['gift_num'] if g['gift_num'] < 30 else 30
                                await WebApi.send_gifts(session, uid=self.uid, bag_id=g['bag_id'], gift_id=g['gift_id'],
                                                        gift_num=gift_num, ruid=self.ruid, room_id=self.room_id,
                                                        csrf=self.csrf)
                                heart_num += gift_num
                            elif g['gift_name'] == '辣条':
                                await WebApi.send_gifts(session, uid=self.uid, bag_id=g['bag_id'], gift_id=g['gift_id'],
                                                        gift_num=g['gift_num'], ruid=self.ruid, room_id=self.room_id,
                                                        csrf=self.csrf)
                                spicy_strips += g['gift_num']
                                await asyncio.sleep(1)
                        if medal['today_feed'] >= 1300:
                            self.message += f"✔ 赠送了{heart_num}个小心心，{spicy_strips}个辣条\n" \
                                            f"目前：{medal['medal_name']}{medal['level']}级\n" \
                                            f"今日亲密度：{medal['today_feed']}/{medal['day_limit']}\n" \
                                            f"当前等级上限：{medal['intimacy']}/{medal['next_intimacy']}\n" \
                                            f"预计还需要{(medal['next_intimacy'] - medal['intimacy']) // medal['today_feed'] + 1}天（{now.strftime('%m.%d')}）到达{medal['level'] + 1}级\n"
                            self.total[0] += 1
                            await asyncio.sleep(1)
                            await self.push()
                        else:
                            if self.request == 0:
                                print("小心心获取未达上限，尝试获取一次\n")
                                self.request -= 1
                            else:
                                self.err_message += "✘ 小心心获取未达上限，且尝试获取失败，请手动检查日志或再次运行\n"
                                self.total[1] += 1
                                await asyncio.sleep(1)
                                await self.push()
                    else:
                        if self.request == 0:
                            print("背包中未发现小心心、辣条，尝试获取一次\n")
                            self.request -= 1
                        else:
                            self.err_message += "✘ 背包中未发现小心心、辣条，且尝试获取失败，请手动检查日志或再次运行\n"
                            self.total[1] += 1
                            await asyncio.sleep(1)
                            await self.push()
                else:
                    print("今日小心心获取已达上限，跳过获取脚本")
                    self.message += f"✔ 今日小心心获取已达上限，跳过获取脚本\n" \
                                    f"目前：{medal['medal_name']}{medal['level']}级\n" \
                                    f"今日亲密度：{medal['today_feed']}/{medal['day_limit']}\n" \
                                    f"当前等级上限：{medal['intimacy']}/{medal['next_intimacy']}\n" \
                                    f"预计还需要{(medal['next_intimacy'] - medal['intimacy']) // medal['today_feed'] + 1}天（{now.strftime('%m.%d')}）到达{medal['level'] + 1}级\n"
                    self.total[0] += 1
                    await asyncio.sleep(1)
                    await self.push()
        else:
            print("未设置赠送对象\n跳过赠送，即将开始获取小心心...")
            self.err_message += "✘ 未设置赠送对象，小心心获取情况请自行查看\n"
            self.total[1] += 1
            self.request -= 1
            await asyncio.sleep(1)
            await self.push()
        await session.close()

    # 重复代码段整合
    async def push(self):
        if self.err_message:
            self.message += f"\n出错日志：\n{self.err_message}"
        if self.sendkey:
            await self.ServerChan()
            print("Server酱已推送")
            await asyncio.sleep(3)

    async def ServerChan(self):
        url = f'https://sctapi.ftqq.com/{self.sendkey}.send'
        data = {
            'title': '直播间打卡推送',
            'desp': self.message.replace('\n', '\n\n')
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data) as resp:
                return await resp.json()

