from email import header
import re
import uuid
import json
import logging
import aiohttp
from .api import WebApi, WebApiRequestError

__VERSION__ = "1.0.1"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("login")


class BiliUser:
    def __init__(
        self, cookie: str, ruid: int, sendkey=None, cloud_service: bool = False
    ):
        self.CLOUD_SERVICE = cloud_service
        if self.CLOUD_SERVICE:
            logger.info("检测到为云函数模式")
        else:
            logger.info("检测到为本地运行模式")
        self.uid = None  # UID
        self.csrf = None  # csrf
        self.buvid = None  # buvid
        self.uname = None  # uname
        self.uuid = uuid.uuid4().hex  # uuid
        self.medal_id = None  # 用户勋章ID
        """
        :param cookie: B站cookie
        :param ruid: 赠送小心心的目标uid
        :param sendkey: serve酱sendkey
        """
        self.cookie = self.check_cookie(cookie)
        self.ruid = ruid

        self.headers = headers = {
            'authority': 'api.bilibili.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': self.cookie,
        }
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.message_err = []  # 错误信息
        self.message = []
        self.room_info = []
        self.room_err_info = []

    def check_cookie(self, cookie):
        """
        检查cookie是否有效
        :return: True or False
        """
        if "LIVE_BUVID=" in cookie and "bili_jct=" in cookie and "DedeUserID=" in cookie:
            if cookie.strip()[-1] != ";":
                cookie += cookie.strip() + ";"
            self.uid = re.search(
                r"DedeUserID=([^;]+);", cookie).group(1).strip()
            self.buvid = re.search(
                r"LIVE_BUVID=([^;]+);", cookie).group(1).strip()
            self.csrf = re.search(
                r"bili_jct=([0-9a-zA-Z]{32})", cookie).group(1).strip()
            return cookie
        else:
            message_err = "缺少关键键值对，cookie无效,重新抓取cookie后重试"
            logger.error(message_err)
            raise WebApiRequestError(message_err)

    async def check_version(self):
        """
        检查版本
        :return:
        """
        url = "https://gitee.com/XiaoMiku01/bili-live-heart/raw/master/version.json"
        res = await self.session.get(url)
        if res.status == 200:
            version_data = json.loads(await res.text())
            if __VERSION__ == version_data["version"]:
                logger.info("检测到当前版本为最新版本(v{})".format(__VERSION__))
            else:
                message = f"当前版本为: v{__VERSION__}, 最新版本为: v{version_data['version']}, 请尽量更新后使用"
                logger.warning(message)
                self.message.append(message)
        else:
            logger.error("检测版本失败")

    async def login(self):
        """
        登录,直播区签到
        :return:
        """
        await self.check_version()
        url = "https://api.bilibili.com/nav"
        res = await self.session.get(url, headers=self.headers)
        if res.status == 200:
            code = res.status
            text = await res.text()
            print("login200_code:", code)
            print("login200_text:", text)
            login_data = await res.json()
            if login_data["code"] == 0:
                self.uname = login_data["data"]["uname"]
                logger.info(
                    "用户: {} (UID:{})登录成功".format(
                        login_data["data"]["uname"], login_data["data"]["mid"]
                    )
                )
                try:
                    sign = await WebApi.do_sign(self.session)
                    message = f"直播区签到成功(本月签到天数:{sign['hadSignDays']}/{sign['allDays']})"
                    logger.info(message)
                    self.message.append(message)
                except WebApiRequestError as e:
                    message_err = f"直播区签到失败: {e}"
                    logger.error(message_err)
                    self.message_err.append(message_err)
        else:
            message_err = "登录失败,重新抓取cookie后重试"
            logger.error(message_err)
            code = await res.status
            text = await res.text()
            logger.error("login_code:", code)
            logger.error("login_text:", text)
            raise WebApiRequestError(message_err)
