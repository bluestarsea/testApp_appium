# -*- coding:utf-8 -*-
"""
run all cases
"""
import unittest
import os
from time import sleep

import readConfig
from commonPac import HTMLTestRunner
from commonPac.AppiumServer import AppiumServer
from commonPac.mydriver import MyDriver

readConfigValue = readConfig.ReadConfig()

class Runtest:
    def __init__(self):
        global resultPath
        resultPath = os.path.join(readConfig.prjPath, "result\\result.html")
        self.casePath = os.path.join(readConfig.prjPath, "caseList")
        # print(self.casePath)
        self.myServer = AppiumServer()

    def driver_on(self):
        MyDriver.get_driver()

    def driver_off(self):
        MyDriver.get_driver().quit()

    # def get_case_list(self):
    #     """
    #     获取所有case
    #     :return:
    #     """
    #     pass

    def create_suite(self):
        """
        将case list 加入到TestSuite中
        :return:
        """
        test_suite = unittest.TestSuite()
        for allcase in os.listdir(rt.casePath):
            casename = os.path.join("%s" % allcase)
            # print(casedir)
            discover = unittest.defaultTestLoader.discover(self.casePath, pattern=casename, top_level_dir=None)
            test_suite.addTest(discover)

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            suites = self.create_suite()

            if suites is not None:
                self.myServer.start_server()

                while not self.myServer.is_running():
                    sleep(1)
                else:
                    self.driver_on()
                    fp = open(resultPath, "wb")
                    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="Report_Title", description="Report_description")
                    runner.run(suites)
                    fp.close()

                    print("all done!")

            else:
                print("create suite failed!")
        except :
            print("running failed!")

        finally:
            # self.driver_off()
            self.myServer.stop_server()


if __name__ == '__main__':
    rt = Runtest()
    rt.run()

