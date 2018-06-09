# -*- coding:utf-8 -*-
"""
读配置文件
"""
import os
import configparser

prjPath = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(prjPath, "config.conf")


class ReadConfig:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def getConfigValue(self, name):
        value = self.cf.get("config", name)
        return value

    def getCMDValue(self, name):
        value = self.cf.get("CMD", name)
        return value

if __name__ == '__main__':
    rc = ReadConfig()
    conf = rc.getConfigValue("deviceName")
    cmdv = rc.getCMDValue("deviceCheck")
    print(conf, cmdv)
    print(prjPath)
    print(configPath)