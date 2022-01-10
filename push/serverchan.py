import logging
import aiohttp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("serverchan")


async def push_message(sendkey, message):
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    data = {"title": f"【粉丝牌助手推送】", "desp": message.replace("\n", "\n\n")}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data):
            pass
    logger.info("Server酱已推送")