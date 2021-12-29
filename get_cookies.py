import json
import logging
import os
import re

import requests
from selenium import webdriver

# 打开配置文件
with open('User/Userinfo.json', 'r', encoding='utf-8') as f:
    USERINFO = json.load(f)

URL = 'http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp'
COOKIES_PATH = 'Cookies/Cookies_DailyReportNWPU.json'
REURL_PAHT = 'User/Reurl.txt'
USERNAME = USERINFO['USERNAME']
PASSWORD = USERINFO['PASSWORD']


def get_cookies():
    # Chrome浏览器
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # 打开网页
    driver.get(URL)
    # 填写表单
    form_username = driver.find_element_by_id('username')
    form_username.send_keys(USERNAME)
    form_password = driver.find_element_by_id('password')
    form_password.send_keys(PASSWORD)
    # 关闭弹窗
    # driver.find_element_by_xpath("//button[@class='el-dialog__headerbtn']").click()
    # 提交
    driver.find_element_by_xpath("//input[@name='submit']").click()
    # 获取cookies
    cookie = driver.get_cookies()
    # print(cookie)
    jsonCookies = json.dumps(cookie)
    with open(COOKIES_PATH, 'w') as f:
        f.write(jsonCookies)
        f.close()
    # 获取重定向的url
    driver.find_element_by_xpath("//i[@class='icon iconfont icon-shangbao1']").click()
    pg_s = driver.page_source
    reurl = re.search(r'(?!ry_util.jsp)\?sign=.*\&timeStamp=\d+', pg_s).group()
    with open(REURL_PAHT, 'w', encoding='utf8') as f:
        f.write(reurl)
    # 退出
    driver.quit()


if __name__ == '__main__':
    get_cookies()
