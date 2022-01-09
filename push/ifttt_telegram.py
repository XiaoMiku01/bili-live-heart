import logging
import aiohttp
import asyncio

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ifttt_telegram")


async def push_message(event_name: str, key: str, message: str):
    resp_text = ''
    ok = False

    # 国内网络环境导致使用IFTTT时大概率会碰到请求发送失败，失败后进行重试能尽最大可能保证请求发送成功
    max_retry = 5
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
    async with aiohttp.ClientSession() as session:
        # 因为retry的语义为失败后的重试次数，那么第一次请求就不应当被认为是一次重试，故为了保证语义正确，此处需要+1
        data = {"value1": "<b>粉丝牌助手推送</b><br>" + message.replace("\n", "<br>")}
        for current_retry in range(max_retry + 1):
            try:
                async with session.post(url=url, json=data) as r:
                    resp_text = await r.text()
                    ok = True
                    break
            except aiohttp.ClientConnectorError as e:
                if current_retry == max_retry:
                    ok = False
                    logger.error(f"网络错误，已进行{max_retry}次重试，不再继续重试。错误详情：{e}")
                else:
                    logger.error(f"网络错误，准备进行第{current_retry + 1}次重试，最多{max_retry}次。错误详情: {e}")
                    await asyncio.sleep(0.2)

    if ok:
        logger.info(f"IFTTT已推送，response: {resp_text}")
    else:
        logger.info("IFTTT推送失败")
