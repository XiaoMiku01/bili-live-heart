import re
import uuid
import logging
import aiohttp
from .api import WebApi, WebApiRequestError

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
        """
        :param cookie: B站cookie
        :param ruid: 赠送小心心的目标uid
        :param sendkey: serve酱sendkey
        """
        self.cookie = self.check_cookie(cookie)
        self.ruid = ruid
        self.sendkey = sendkey

        self.headers = {
            "Referer": "https://live.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36",
            "Cookie": self.cookie,
        }
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.message_err = []  # 错误信息
        self.message = []
        self.room_info = []

    def check_cookie(self, cookie):
        """
        检查cookie是否有效
        :return: True or False
        """
        if "LIVE_BUVID=" in cookie and "bili_jct=" in cookie:
            self.uid = re.search(r"DedeUserID=([^;]+);", cookie).group(1)
            self.buvid = re.search(r"LIVE_BUVID=([^;]+);", cookie).group(1)
            self.csrf = re.search(r"bili_jct=([^;]+);", cookie).group(1)
            return cookie
        else:
            logger.error("cookie无效,请`关闭`浏览器`无痕模式`重新抓取cookie后重试")
            raise

    async def login(self):
        """
        登录,直播区签到
        :return:
        """
        url = "https://api.bilibili.com/nav"
        res = await self.session.post(url)
        if res.status == 200 and (login_data := await res.json())["code"] == 0:
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
            logger.error("登录失败,请`关闭`浏览器`无痕模式`重新抓取cookie后重试")
            raise
