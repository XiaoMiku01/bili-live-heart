import asyncio
import json
import sys
import time
from run import main
from Daily import Live


def main_handler(event, context):
    print("start!")
    data = json.loads(context['environment'])
    uid, cookie = data['uid'], data['cookie']
    ruid = data.get('ruid', None)
    sendkey = data.get('sendkey', None)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(uid, cookie, cloud_service=True))
    except Exception as e:
        print(f"运行出错:{repr(e)}")
        return False
    time.sleep(10)
    l = Live(uid, cookie, ruid, sendkey)
    loop.run_until_complete(l.run())
    print(l.message)
    print('complete!')
    return True


if __name__ == '__main__':
    import toml

    user_config = toml.load('./user.toml')
    u = user_config['users']
    uid = u['uid']
    cookie = u['cookie']
    ruid = u.get('ruid', None)
    sendkey = u.get('sendkey', None)
    assert uid and cookie, "用户配置不能为空"
    print("start!")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(uid, cookie, cloud_service=False))
    except Exception as e:
        print(f"运行出错:{repr(e)}")
        sys.exit(1)
    time.sleep(10)
    l = Live(uid, cookie, ruid, sendkey)
    loop.run_until_complete(l.run())
    print(l.message)
    print('complete!')
