import asyncio
import json
import sys
import time
from run import main
from Daily import Live


def main_handler(event, context):   # 运行逻辑顺序有修改，详见README.md，下同
    print("Start!")
    data = json.loads(context['environment'])
    uid, cookie = data['uid'], data['cookie']
    ruid = data.get('ruid', None)
    sendkey = data.get('sendkey', None)
    l = Live(uid, cookie, ruid, sendkey)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(l.run())
    time.sleep(10)
    loop.run_until_complete(l.gift())
    time.sleep(10)
    if l.request == -1:
        try:
            time.sleep(10)
            loop.run_until_complete(main(uid, cookie, cloud_service=True))
            time.sleep(10)
            loop.run_until_complete(l.gift())
            time.sleep(10)
        except Exception as e:
            print(f"运行出错:{repr(e)}")
            return False
    print(l.message)
    print('Complete!')
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
    print("Start!")
    l = Live(uid, cookie, ruid, sendkey)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(l.run())
    time.sleep(10)
    loop.run_until_complete(l.gift())
    time.sleep(10)
    if l.request == -1:
        try:
            time.sleep(10)
            loop.run_until_complete(main(uid, cookie, cloud_service=False))
            time.sleep(10)
            loop.run_until_complete(l.gift())
            time.sleep(10)
        except Exception as e:
            print(f"运行出错:{repr(e)}")
            sys.exit(1)
    time.sleep(10)
    print(l.message)
    print('Complete!')
