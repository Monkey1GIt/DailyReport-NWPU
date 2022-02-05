# coding=utf-8
# @time         2022-02-05 230637
# @author       Monkey_NWPU
# @function     自动批量每日疫情填报
# @debug
# @init         2020-12-12 230343


import json
import logging
import os

import requests


class AutoSignin():
    def __init__(self):
        # logging配置
        log_format = '[%(asctime)s] - %(levelname)s\t> %(message)s'
        log_filename = 'opt.log'
        log_hander = [logging.FileHandler(log_filename, 'a', 'utf8')]
        logging.basicConfig(level=logging.INFO,
                            format=log_format, handlers=log_hander)
        # session
        self.req_session = requests.session()
        # 忽略ssl警告
        requests.packages.urllib3.disable_warnings()
        self.context = {}

    def get_paramas(self):
        '''读取cookie和header
        '''
        # 获取headers
        with open('Headers/Headers_' + self.context['name'] + '.json', 'r') as f:
            self.headers = json.load(f)
        # self.req_session.headers = self.headers
        # self.req_session.headers.update(self.headers)
        # 获取cookies
        self.jar_cookies = requests.cookies.RequestsCookieJar()
        with open('Cookies/Cookies_' + self.context['name'] + '.json', 'r') as f:
            cookies_json = json.load(f)
        for cookie in cookies_json:
            self.jar_cookies.set(cookie['name'], cookie['value'])
        # self.req_session.headers = self.jar_cookies

    def mk_req(self):
        '''构造http请求
        '''
        try:
            # http post get
            if self.context['method'] == 'GET':
                r = self.req_session.get(
                    self.context['url'],  headers=self.headers, cookies=self.jar_cookies, verify=False, timeout=3)
            elif self.context['method'] == 'POST':
                r = self.req_session.post(
                    self.context['url'], headers=self.headers, cookies=self.jar_cookies, data=self.context['data'], verify=False, timeout=3)
            # print(r.text)
            self.http_response = r
        except Exception as e:
            msg_error = 'mk_req: ' + e.__class__.__name__ + ': ' + str(e)
            print(msg_error)
            logging.error(msg_error)

    def tell_res(self, data):
        '''根据配置文件, 判断http请求是否成功
        Args:
            data: http请求报文
        Return:
            None
        '''
        flag_new = True
        for example in self.context['response']:
            if data.find(example['text']) > -1:
                status = example['status']
                info = example['info']
                flag_new = False
                break
        # 如果出现新的respone
        if flag_new:
            status = 'NO'
            info = data.replace('\n', '')
            info = info.replace('\t', '')
            info = info.replace('\r', '')
            info = info[0:120]
            print(info[0:500])
        # log
        out_text = f'{self.context["name"]}: {status}: {info}'
        logging.info(out_text)
        print(out_text, flush=True)


if __name__ == '__main__':
    sign_1 = AutoSignin()
