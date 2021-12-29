import json

from auto_signin import AutoSignin
from get_cookies import get_cookies


def run():
    # 打开配置文件
    with open('User/Context.json', 'r', encoding='utf-8') as f:
        context_json = json.load(f)
    # selenium 获取cookies
    get_cookies()
    # 获取重定向url
    with open('User/Reurl.txt', 'r', encoding='utf8') as f:
        reurl = f.read()
    # 自动签到
    signin = AutoSignin()
    signin.context = context_json[0]
    signin.get_paramas()
    for context in context_json:
        signin.context = context
        signin.context['url'] = signin.context['url'] + reurl
        signin.mk_req()
        signin.res_tell(signin.http_response.text)
        # print(signin.http_response.status_code)
        # print(signin.http_response.text)


if __name__ == '__main__':
    run()
