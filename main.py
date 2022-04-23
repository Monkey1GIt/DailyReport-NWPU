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
USERNAME = USERINFO['USERNAME']
PASSWORD = USERINFO['PASSWORD']

# logging配置
log_format = '[%(asctime)s] - %(levelname)s\t> %(message)s'
log_filename = 'opt.log'
log_hander = [logging.FileHandler(log_filename, 'a', 'utf8')]
logging.basicConfig(level=logging.INFO,
                    format=log_format, handlers=log_hander)


def get_cookies():
    status = 'NO'
    info = ''
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
    try:
        # 获取重定向的url
        driver.find_element_by_xpath("//i[@class='icon iconfont icon-shangbao1']").click()
    except Exception as e:
        # msg_error = 'get_cookies: ' + e.__class__.__name__ + ': ' + str(e)
        if e.__class__.__name__.find('NoSuchElementException') > -1:
            if driver.page_source.find('账号或密码错误') > -1:
                info = '账号或密码错误'
            else:
                info = driver.page_source[:200]
            return status, info
    # 
    if driver.page_source.find('您已提交今日填报') > -1:
        status = 'OK'
        info = 'Have Signed!'
        return status, info
    # 模拟点击
    driver.find_element_by_xpath("//a[@class='weui-btn weui-btn_primary']").click()
    driver.find_element_by_xpath("//i[@class='weui-icon-checked']").click()
    driver.find_element_by_xpath("//a[@id='save_div']").click()
    # 判断状态
    if driver.page_source.find('您已提交今日填报') > -1:
        status = 'OK'
        info = ''
    else:
        status = 'NO'
        info = '自动提交失败'
    # 退出
    driver.quit()
    return status, info


if __name__ == '__main__':
    status, info = get_cookies()
    # log
    out_text = f'NWPU每日疫情填报: {status}: {info}'
    logging.info(out_text)
    print(out_text)