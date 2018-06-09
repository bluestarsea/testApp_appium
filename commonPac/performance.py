#-*-coding:utf-8-*-
import os
import re
import xlrd
import xlwt
from xlutils.copy import copy
import datetime

global date_today
date_today = str(datetime.date.today())

class Device_Exception(Exception):
    '''
    自定义异常：没有连接设备
    '''
    pass

class Start_Exception(Exception):
    '''
    自定义异常：没有启动目标app
    '''
    pass

#性能数据采集
class PerformanceData:

    def __init__(self):
        pass

    def creat_xlsx(self,num):
        '''
        创建xlsx文件，保存采集数据
        :param num:
        :return:
        '''
        book = xlwt.Workbook(encoding='utf-8')
        s = book.add_sheet('collection_data')
        if num == 0:
            s.write(0, 0, 'Total')
            s.write(0, 1, 'Native Heap')
            s.write(0, 2, 'Dalvik Heap')
            book.save('../result/mem' + date_today + '.xlsx')
        elif num == 1:
            s.write(0, 0, 'cpu')
            s.write(0, 1, 'user')
            s.write(0, 2, 'kernel')
            book.save('../result/cpu' + date_today + '.xlsx')
        elif num == 2:
            s.write(0, 0, 'rx-byte(kb)')
            s.write(0, 1, 'tx-byte(kb)')
            book.save('../result/flow' + date_today + '.xlsx')

    def get_uid(self,packagename):
        '''
        获取目标app在当前手机上的uid
        :param packagename:
        :return:
        '''
        try:
            device = os.popen('adb devices').readlines()
            if device[1].strip() == '':
                raise Device_Exception
        except Device_Exception:
            print('Device not find')
        else:
            try:
                command = 'adb shell ps | find \"{0}\"'.format(packagename)
                results = os.popen(command).readlines()
                if len(results) == 0:
                    raise Start_Exception
            except Start_Exception:
                return 0
            else:
                uid = results[0].split(' ')[0]
                print(uid)
                return str(10000 + int(uid[4:]))

    def mem_info(self,packagename, num):
        '''
        采集当前场景下的内存数据
        :param packagename:
        :param num:
        :return:
        '''
        try:
            device = os.popen('adb devices').readlines()
            if device[1].strip() == '':
                raise Device_Exception
        except Device_Exception:
            print('Device not find')
        else:
            try:
                command = 'adb shell dumpsys meminfo {0}'.format(packagename)
                results = os.popen(command).readlines()
                if results[0].strip() == 'No process found for: com.jiankecom.jiankemall':
                    raise Start_Exception
            except Start_Exception:
                print('App not start')
            else:
                date_today = str(datetime.date.today())
                for result in results:
                    if re.search('Native Heap',result) is not None:
                        native = re.findall(r"\d+\.?\d*", result)
                    if re.search('Dalvik Heap',result) is not None:
                        dalvik = re.findall(r"\d+\.?\d*", result)
                    if re.search('TOTAL',result) is not None:
                        total = re.findall(r"\d+\.?\d*", result)
                book = xlrd.open_workbook('../result/mem' + date_today + '.xlsx', formatting_info=True)
                book1 = copy(book)
                s = book1.get_sheet(0)
                s.write(num, 0, total[0])
                s.write(num, 1, native[0])
                s.write(num, 2, dalvik[0])
                book1.save('../result/mem' + date_today + '.xlsx')

    def cpu_info(self,packagename, num):
        '''
        采集当前场景下的cpu使用率
        :param packagename:
        :param num:
        :return:
        '''
        try:
            device = os.popen('adb devices').readlines()
            if device[1].strip() == '':
                raise Device_Exception
        except Device_Exception:
            print('Device not find')
        else:
            try:
                command = 'adb shell dumpsys cpuinfo | find \"{0}\"'.format(packagename)
                results = os.popen(command).readlines()
                if len(results) == 0:
                    raise Start_Exception
            except Start_Exception:
                print('App not start')
            else:
                # date_today = str(datetime.date.today())
                r = results[0].split(' ')
                book = xlrd.open_workbook('../result/cpu' + date_today + '.xlsx ', formatting_info=True)
                book1 = copy(book)
                s = book1.get_sheet(0)
                s.write(num, 0, r[2])  # cpu使用率
                s.write(num, 1, r[4])  # user占用率
                s.write(num, 2, r[7])  # kernel占用率
                book1.save('../result/cpu' + date_today + '.xlsx')

    # 耗电量
    def battery_info(self):
        '''
        采集电量数据
        :return:
        '''
        command = 'adb shell dunpsys batterystats --reset'
        os.system(command)

    def flot_info(self,packagename,num):
        '''
        采集流量数据
        :param num:
        :return:
        '''
        try:
            device = os.popen('adb devices').readlines()
            if device[1].strip() == '':
                raise Device_Exception
        except Device_Exception:
            print('Device not find')
        else:
            try:
                uid = self.get_uid(packagename)
                if uid == 0:
                    raise Start_Exception
            except Start_Exception:
                print('App not start')
            else:
                command = 'adb shell cat /proc/net/xt_qtaguid/stats | find \"{0}\"'.format(uid)
                results = os.popen(command).readlines()
                rx = 0
                tx = 0
                for result in results:
                    if result.strip() != '':
                        rx += int(result.split(' ')[5].strip())
                        tx += int(result.split(' ')[7].strip())
                book = xlrd.open_workbook('../result/flow' + date_today + '.xlsx', formatting_info=True)
                book1 = copy(book)
                s = book1.get_sheet(0)
                s.write(num, 0, rx / 1024)
                s.write(num, 1, tx / 1024)
                book1.save('../result/flow' + date_today + '.xlsx')

    def all_performance(self,packagename,num):
        self.cpu_info(packagename,num)
        self.mem_info(packagename,num)
        self.flot_info(packagename,num)

    #处理flot文件
    def reflot(self):
        '''
        flot.xlsx中的数据是app产生的总流量，要获取每个场景使用的流量，需要对获取到的数据进行处理:
        使用的流量=当前场景获取的总流量-前一个场景获取的总流量
        :return:
        '''
        book=xlrd.open_workbook('../result/flow' + date_today + '.xlsx')
        s=book.sheet_by_index(0)
        rx=s.col_values(0)
        tx=s.col_values(1)
        pass

if __name__=='__main__':
    a=PerformanceData()
    #for i in range(3):
        #a.creat_xlsx(i)
    a.all_performance('com.jiankecom.jiankemall',3)