# coding=utf-8
# @time         2021-08-04 214900
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
        # 忽略ssl警告
        requests.packages.urllib3.disable_warnings()
        # logging配置
        log_format = '[%(asctime)s] - %(levelname)s\t> %(message)s'
        log_filename = 'opt.log'
        log_hander = [logging.FileHandler(log_filename, 'a', 'utf8')]
        logging.basicConfig(level=logging.INFO,
                            format=log_format, handlers=log_hander)

    def run(self):
        self.get_paramas()
        self.res = self.mk_req()

    def get_paramas(self, context):
        '''从文件中读取cookie和header
            Args:
                context: 输入的requests参数
        '''
        self.context = context
        # 获取headers
        with open('Headers/Headers_' + self.context['name'] + '.json', 'r') as f:
            self.headers = json.load(f)
            f.close()
        # 获取cookies
        self.jar_cookies = requests.cookies.RequestsCookieJar()
        with open('Cookies/Cookies_' + self.context['name'] + '.json', 'r') as f:
            cookies_json = json.load(f)
            f.close()
        for cookie in cookies_json:
            self.jar_cookies.set(cookie['name'], cookie['value'])

    def mk_req(self):
        '''构造http请求
        '''
        try:
            # http post get
            if self.context['method'] == 'GET':
                r = requests.get(self.context['url'], headers=self.headers,
                                 cookies=self.jar_cookies, verify=False, timeout=3)
            elif self.context['method'] == 'POST':
                r = requests.post(self.context['url'], headers=self.headers,
                                  cookies=self.jar_cookies, data=self.context['data'], verify=False, timeout=3)
            # 判断结果
            self.http_r = r
        except Exception as e:
            msg_error = 'mk_req: ' + e.__class__.__name__ + ': ' + str(e)
            print(msg_error)
            logging.error(msg_error)

    def res_tell(self, data):
        '''判断结果
        Args:
            data: http请求结果
        '''
        if data.find(self.context['result']) > -1:
            res = 'OK'
        else:
            flag = True
            res = 'NO: '
            for err in self.context['error']:
                if data.find(err) > -1:
                    res = res + self.context['error'][err]
                    flag = False
            if flag:
                print(data)
        res_dict = {self.context['name']: res}
        logging.info(res_dict)
        return res


if __name__ == '__main__':
    sign_1 = AutoSignin()
