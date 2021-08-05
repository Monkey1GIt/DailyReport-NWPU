import json

from auto_signin import AutoSignin


class DailyReport(AutoSignin):
    def __init__(self):
        super().__init__()
        # 打开配置文件
        with open('Context.json', 'r', encoding='utf-8') as f:
            self.context_json = json.load(f)

    def run(self):
        self.get_cookies()
        # self.get_paramas()
        # self.res = self.mk_req()

        # 先获取cookies
    def get_cookies(self):
        context = self.context_json['cookies_param']
        self.get_paramas(context)
        self.mk_req()
        print(self.http_r.status_code)
        # print(self.http_r.text)
        print(self.http_r.cookies)


if __name__ == '__main__':
    report_1 = DailyReport()
    report_1.run()
