# -*- coding: utf-8 -*-
"""
Configure the Appium Service:start, stop, catch status...
"""
import os
import readConfig
import threading
import urllib.request
from urllib.error import URLError
from multiprocessing import Process
from time import sleep

readConfigValue = readConfig.ReadConfig()


class AppiumServer:

    def __init__(self):
        global openAppium, baseUrl
        openAppium = readConfigValue.getCMDValue("openAppium")
        baseUrl = readConfigValue.getConfigValue("baseUrl")

    def start_server(self):
        '''
        launch appium node server:
         start /b node D:\Appium\node_modules\appium\lib\server\main.js --address 127.0.0.1 --port 4723
        :return:
        '''
        t = RunServer(openAppium)
        p = Process(target=t.start())
        p.start()

    def stop_server(self):
        cmd = 'netstat -aon | findstr "4723" '
        result = os.popen(cmd).readlines()[0]
        pid = str(result[71:len(result)-1])
        cmd2 = "taskkill /F /pid "+pid
        os.popen(cmd2)

    def is_running(self):
        response = None
        url = baseUrl + "/status"
        try:
            response = urllib.request.urlopen(url, timeout=10)

            if str(response.getcode()).startswith("2"):
                return True
            else:
                return False
        except URLError:
            return False
        finally:
            if response:
                response.close()


class RunServer(threading.Thread):

    def __init__(self, cmd):
        self.cmd = cmd
        threading.Thread.__init__(self)

    def run(self):
        print("Wait for Appium running...")
        os.system(self.cmd)

if __name__ == '__main__':
    rs = AppiumServer()
    rs.start_server()
    print("start server")
    print("running server")
    sleep(20)
    rs.stop_server()
    print("killed successfully")

