#!/usr/bin/env python3
import re
import uuid
import asyncio
from collections import namedtuple
from asyncio import CancelledError

import aiohttp

from api import WebApi

if not hasattr(asyncio, 'create_task'):
    asyncio.create_task = asyncio.ensure_future

if not hasattr(asyncio, 'get_running_loop'):
    asyncio.get_running_loop = asyncio.get_event_loop


async def get_info(session, room_id):
    try:
        info = await WebApi.get_info(session, room_id)
    except CancelledError:
        raise
    except Exception:
        info = await WebApi.get_info_by_room(session, room_id)
        info = info['room_info']

    return info


async def medals(session):
    page = 1

    while True:
        data = await WebApi.get_medal(session, page=page)
        page_info = data['page_info']
        assert page == page_info['cur_page']

        for medal in data['items']:
            if medal['roomid'] == 0:
                continue
            yield medal

        if page < page_info['total_page']:
            page += 1
        else:
            break


def extract_csrf(cookie):
    try:
        return re.search(r'bili_jct=([^;]+);', cookie).group(1)
    except Exception:
        return None


def extract_buvid(cookie):
    try:
        return re.search(r'LIVE_BUVID=([^;]+);', cookie).group(1)
    except Exception:
        return None


async def obtain_buvid(cookie):
    async with aiohttp.request('GET', 'https://live.bilibili.com/3',
                               headers={'Cookie': cookie}) as res:
        return extract_buvid(str(res.cookies['LIVE_BUVID']))


class User:
    count = 1

    def __init__(self, name, cookie, csrf, buvid, uuid):
        cls = self.__class__
        self.name = name
        # self.num = cls.count
        self.num = ''
        cls.count += 1
        self.cookie = cookie
        self.csrf = csrf
        self.uuid = uuid
        self.buvid = buvid


RoomInfo = namedtuple('RoomInfo', 'room_id, parent_area_id, area_id')


class SmallHeartTask:
    def __init__(self, user: User, cloud_service: bool = False):
        self.user = user
        self.MAX_HEARTS_PER_DAY = 24
        self.MAX_CONCURRENT_ROOMS = self.MAX_HEARTS_PER_DAY
        self.HEART_INTERVAL = 300
        self.CLOUD_SERVICE = cloud_service
        if self.CLOUD_SERVICE:
            print('检测到为云函数模式')
        else:
            print('检测到为本地运行模式')

    async def do_work(self):
        global session

        uname = self.user.name
        num = self.user.num
        MAX_HEARTS_PER_DAY = self.MAX_HEARTS_PER_DAY

        headers = {
            'Referer': 'https://live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36',
            'Cookie': self.user.cookie,
        }
        self.session = session = aiohttp.ClientSession(headers=headers)
        try:
            print(f'开始今天的小心心任务（用户{num}：{uname}）')

            room_infos = []
            count = 0

            async for m in medals(session):
                try:
                    info = await get_info(session, m['roomid'])
                except KeyError:
                    continue
                room_id = info['room_id']  # ensure not the short id
                area_id = info['area_id']
                parent_area_id = info['parent_area_id']
                room_info = RoomInfo(room_id, parent_area_id, area_id)

                if parent_area_id == 0 or area_id == 0:
                    print(
                        f'Invalid room info（用户{num}：{uname}）: {room_info}')
                    continue

                room_infos.append(room_info)
                count += 1

                if count == self.MAX_CONCURRENT_ROOMS:
                    break

            if len(room_infos) == 0:
                raise Exception(f'一个勋章都没有~结束任务（用户{num}：{uname}）')
            # if (len(room_infos) < 8) and self.CLOUD_SERVICE:
            #     raise Exception(
            #         f'粉丝牌不足9个，云函数无法执行，请在本地运行~结束任务（用户{num}：{uname}）')
            self.queue = queue = asyncio.Queue(MAX_HEARTS_PER_DAY)

            for i in range(1, MAX_HEARTS_PER_DAY + 1):
                queue.put_nowait(i)

            dispatcher = asyncio.create_task(self.dispatch(room_infos))

            await queue.join()
            print(f'今天小心心任务已完成（用户{num}：{uname}）')
            return
        except CancelledError:
            raise
        finally:
            try:
                dispatcher.cancel()
            except Exception:
                pass

            try:
                for task in self.tasks:
                    task.cancel()
            except Exception:
                pass

            await session.close()

    async def dispatch(self, room_infos):
        uname = self.user.name
        num = self.user.num
        self.tasks = tasks = []

        for room_info in room_infos:
            task = asyncio.create_task(self.post_heartbeats(*room_info))
            tasks.append(task)
            print(f'{room_info.room_id}号直播间心跳任务开始（用户{num}：{uname}）')

    async def post_heartbeats(self, room_id, parent_area_id, area_id):
        session = self.session
        csrf = self.user.csrf
        buvid = self.user.buvid
        uuid = self.user.uuid
        uname = self.user.name
        num = self.user.num
        queue = self.queue

        while True:
            sequence = 0

            try:
                result = await WebApi.post_enter_room_heartbeat(session, csrf, buvid, uuid, room_id, parent_area_id,
                                                                area_id)
                print(f'进入{room_id}号直播间心跳已发送（用户{num}：{uname}）')
                # print(
                #     f'进入{room_id}号直播间心跳发送结果（用户{num}：{uname}）: {result}')

                while True:
                    sequence += 1
                    interval = result['heartbeat_interval']
                    print(
                        f'{interval}秒后发送第{sequence}个{room_id}号直播间内心跳（用户{num}：{uname}）')
                    await asyncio.sleep(interval)

                    result = await WebApi.post_in_room_heartbeat(
                        session, csrf, buvid, uuid,
                        room_id, parent_area_id, area_id,
                        sequence, interval,
                        result['timestamp'],
                        result['secret_key'],
                        result['secret_rule'],
                    )

                    print(
                        f'第{sequence}个{room_id}号直播间内心跳已发送（用户{num}：{uname}）')
                    # print(
                    #     f'第{sequence}个{room_id}号直播间内心跳发送结果（用户{num}：{uname}）: {result}')

                    assert self.HEART_INTERVAL % interval == 0, interval
                    heartbeats_per_heart = self.HEART_INTERVAL // interval

                    if sequence % heartbeats_per_heart == 0:
                        n = queue.get_nowait()
                        print(f'获得第{n}个小心心（用户{num}：{uname}）')
                        queue.task_done()
            except asyncio.QueueEmpty:
                print(
                    f'小心心任务已完成, {room_id}号直播间心跳任务终止。（用户{num}：{uname}）')
                break
            except CancelledError:
                # print(f'{room_id}号直播间心跳任务取消（用户{num}：{uname}）')
                raise
            except Exception as e:
                if sequence == 0:
                    print(
                        f'进入{room_id}号直播间心跳发送异常（用户{num}：{uname}）: {repr(e)}')
                else:
                    print(
                        f'第{sequence}个{room_id}号直播间内心跳发送异常（用户{num}：{uname}）: {repr(e)}')

                delay = 60
                print(f'{delay}秒后重试{room_id}号直播间心跳任务（用户{num}：{uname}）')
                await asyncio.sleep(delay)


async def main(uid, cookie, cloud_service=False):
    csrf = extract_csrf(cookie)
    buvid = extract_buvid(cookie) or await obtain_buvid(cookie)
    user = User(uid, cookie, csrf, buvid, uuid.uuid4())
    await SmallHeartTask(user, cloud_service).do_work()
