# -*- coding:utf-8 -*-
"""
获取、打开driver
"""
import readConfig
import os
from appium import webdriver
from selenium.common.exceptions import WebDriverException
from urllib.error import URLError

readConfigValue = readConfig.ReadConfig()


class MyDriver:

    driver = None
    deviceName = readConfigValue.getConfigValue("deviceName")
    platformName = readConfigValue.getConfigValue("platformName")
    platformVersion = readConfigValue.getConfigValue("platformVersion")
    appPackage = readConfigValue.getConfigValue("appPackage")
    appActivity = readConfigValue.getConfigValue("appActivity")
    baseUrl = readConfigValue.getConfigValue("baseUrl")
    app = os.path.join(os.path.dirname(__file__), "jiankemall.apk")

    desired_caps = {
        "deviceName": deviceName,
        "platformName": platformName,
        "platformVersion": platformVersion,
        "app": app
    }

    def __init__(self):
        pass

    @staticmethod
    def get_driver():
        try:
            if MyDriver.driver is None:
                try:
                    MyDriver.driver = webdriver.Remote(MyDriver.baseUrl, MyDriver.desired_caps)
                except URLError:
                    # MyDriver.driver = None
                    print("URLError")

            return MyDriver.driver
        except WebDriverException:
            raise

if __name__ == '__main__':
    md = MyDriver()
    # print(webdriver.Remote(MyDriver.baseUrl, MyDriver.desired_caps))
    # print(md.get_driver())
    # print(MyDriver.baseUrl)
