import logging
from onepush import notify

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("pushaio")


def notify_me(config, title, content):
    notifier = config.get('notifier')
    params = config.get('params')
    if not notifier or not params:
        logger.info('没有配置通知方法...')
        return
    logger.info('正在准备发送通知...')
    return notify(notifier, title=title, content=content, **params)
