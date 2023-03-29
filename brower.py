#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Jiong.L
@time: 2023/3/29 21:15
"""
from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {
    'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '8',  # 手机安卓版本
    'deviceName': 'Mi_10',  # 设备名，安卓手机可以随意填写
    'appPackage': 'mark.via',  # 启动APP Package名称
    'appActivity': 'mark.via.Shell',  # 启动Activity名称
    'noReset': True,  # 不要重置App
    'newCommandTimeout': 10000,
    'automationName': 'UiAutomator2',
    # 'chromeOptions': {'w3c': False}
}

# 连接Appium Server，初始化自动化环境
# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver = webdriver.Remote('http://docker.jokerin.icu:4723/wd/hub', desired_caps)

# 设置缺省等待时间
driver.implicitly_wait(5)

driver.find_element(By.ID, 'as').click()
driver.find_element(By.XPATH, '//android.webkit.WebView/android.view.View/android.view.View[2]/android.widget.EditText').send_keys('http://118.24.62.239:9980/')
pass
