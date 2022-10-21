import json
import logging
import os
import re
import sys

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


FLAG_DEBUG = False
URL = 'http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp'
# 输入传递参数
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
# logging配置
log_format = '[%(asctime)s] - %(levelname)s\t> %(message)s'
log_filename = 'opt.log'
log_hander = [logging.FileHandler(log_filename, 'a', 'utf8')]
logging.basicConfig(level=logging.INFO,
                    format=log_format, handlers=log_hander)


def submit_form():
    status = 'NO'
    info = ''
    # Chrome浏览器
    user_options = webdriver.ChromeOptions()
    if not FLAG_DEBUG:
        user_options.add_argument('--headless')
    driver = webdriver.Chrome(options=user_options)
    # 打开网页
    driver.get(URL)
    # 填写表单
    form = driver.find_element_by_xpath('//li[contains(text(),"密码")]')
    form.click()
    form_username = driver.find_element_by_xpath(
        '//form[@id="fm1"]//input[@id="username"]')
    form_username.send_keys(USERNAME)
    form_password = driver.find_element_by_xpath(
        '//form[@id="fm1"]//input[@id="password"]')
    form_password.send_keys(PASSWORD)
    # 关闭弹窗
    # driver.find_element_by_xpath("//button[@class='el-dialog__headerbtn']").click()
    # 提交
    btn_submit = driver.find_element_by_xpath(
        '//input[@name="button" and @accesskey="l"]')
    btn_submit.click()
    # 显示等待页面跳转
    WebDriverWait(driver, 3).until(EC.title_is('疫情每日填报'))
    # 查询登录状态
    if driver.page_source.find('疫情每日填报') == -1:
        # msg_error = 'submit_form: ' + e.__class__.__name__ + ': ' + str(e)
        if driver.page_source.find('账号或密码错误') > -1:
            info = '账号或密码错误'
        else:
            info = driver.page_source[:200]
        return status, info
    # 检查提交状态
    if driver.page_source.find('您已提交今日填报') > -1:
        status = 'OK'
        info = 'Have Signed!'
        return status, info
    # 模拟点击
    driver.find_element_by_xpath(
        '//a[@class="weui-btn weui-btn_primary"]').click()
    driver.find_element_by_xpath(
        '//label[@class="weui-cell weui-cell_active weui-check__label"]').click()
    driver.find_element_by_xpath('//a[@id="save_div"]').click()
    # 判断状态
    driver.get('https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp')
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
    status, info = submit_form()
    # log
    out_text = f'NWPU每日疫情填报: {status}: {info}'
    logging.info(out_text)
    print(out_text)
