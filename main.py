import json

from auto_signin import AutoSignin
from get_cookies import get_cookies


def run():
    # 打开配置文件
    with open('User/Context.json', 'r', encoding='utf-8') as f:
        context_json = json.load(f)
    # selenium 获取cookies
    get_cookies()
    # 自动签到
    signin = AutoSignin()
    signin.context = context_json[0]
    signin.get_paramas()
    for context in context_json:
        signin.context = context
        signin.mk_req()
        signin.res_tell(signin.http_response.text)
        # print(signin.http_response.status_code)
        # print(signin.http_response.text)


if __name__ == '__main__':
    run()
