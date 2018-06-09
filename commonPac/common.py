#! python3
# -*- coding: utf-8 -*-
"""
common operations about device and elements
"""
import os
from xml.etree import ElementTree as ET
from selenium.common.exceptions import NoSuchElementException

import readConfig
from commonPac.mydriver import MyDriver

readConfigValue = readConfig.ReadConfig()


def get_window_size(driver,during=None):
    global windowSize
    windowSize = driver.get_window_size()
    return windowSize

def swipe_to_up(driver,during=None):
    gws = get_window_size()
    width = gws.get("width")
    height = gws.get("height")
    driver.swipe(width/2, height*0.75, width/2, height*0.25, during)

def swipe_to_down(driver,during=None):
    gws = get_window_size()
    width = gws.get("width")
    height = gws.get("height")
    driver.swipe(width/2, height*0.25, width/2, height*0.75, during)

def swipe_to_left(driver,during=None):
    gws = get_window_size()
    width = gws.get("width")
    height = gws.get("height")
    driver.swipe(width*0.75, height/2, width*0.25, height/2, during)

def swipe_to_right(driver,during=None):
    gws = get_window_size()
    width = gws.get("width")
    height = gws.get("height")
    driver.swipe(width*0.25, height/2, width*0.75, height/2, during)

def back():
    os.popen("adb shell input keyevent 4")

def hidekeyboard(driver):
    driver.hide_keyboard()

def shake(driver):
    driver.shake()

activity = {}


# get activity_name and element_name from xml
def get_xml():

    if len(activity) == 0:
        xml_path = os.path.join(readConfig.prjPath, "commonPac", "element.xml")
        all_element = ET.parse(xml_path).findall("activity")

        for element1 in all_element:
            activity_name = element1.get("name")

            element = {}
            for element2 in element1.getchildren():
                element_name = element2.get("name")

                element_child = {}
                for element3 in element2.getchildren():
                    element_child[element3.tag] = element3.text

                element[element_name] = element_child
            activity[activity_name] = element
    return activity

def set_element_dict(activity_name, element_name):
    activity=get_xml()
    element_dict = activity.get(activity_name).get(element_name)
    return element_dict


class Element:
    '''
    using: Element(activity_name,element_name).click()
    '''

    def __init__(self, activity_name, element_name,driver):
        self.driver=driver
        self.activity_name = activity_name
        self.element_name = element_name
        element_dict = set_element_dict(self.activity_name, self.element_name)
        self.pathtype = element_dict.get("pathtype")
        self.pathvalue = element_dict.get("pathvalue")

    def get_element(self):
        try:
            if self.pathtype == "ID":
                element = self.driver.find_element_by_id(self.pathvalue)
                return element
            if self.pathtype == "NAME":
                element = self.driver.find_element_by_name(self.pathvalue)
                return element
            if self.pathtype == "XPATH":
                element = self.driver.find_element_by_xpath(self.pathvalue)
                return element
            if self.pathtype == "CLASSNAME":
                element = self.driver.find_element_by_class_name(self.pathvalue)
                return element
        except NoSuchElementException:
            raise

    def get_elements(self):  # not in used temporarily
        try:
            if self.pathtype == "ID":
                elements = self.driver.find_elements_by_id(self.pathvalue)
                return elements
            if self.pathtype == "NAME":
                elements = self.driver.find_elements_by_name(self.pathvalue)
                return elements
            if self.pathtype == "XPATH":
                elements = self.driver.find_elements_by_xpath(self.pathvalue)
                return elements
            if self.pathtype == "CLASSNAME":
                elements = self.driver.find_elements_by_class_name(self.pathvalue)
                return elements
        except NoSuchElementException:
            raise

    def is_exist(self):
        """
        do exist: True
        not exist: False
        :return:
        """

        try:
            if self.pathtype == "ID":
                self.driver.find_element_by_id(self.pathvalue)
                return True
            if self.pathtype == "NAME":
                self.driver.find_elements_by_name(self.pathvalue)
                return True
            if self.pathtype == "XPATH":
                self.driver.find_element_by_xpath(self.pathvalue)
                return True
            if self.pathtype == "CLASSNAME":
                self.driver.find_element_by_class_name(self.pathvalue)
                return True
            return False
        except NoSuchElementException:
            return False

    def click(self):
        try:
            element = self.get_element()
            element.click()
        except AttributeError:
            raise

    def send_keys(self, values):
        try:
            element = self.get_element()
            element.send_keys(values)
        except AttributeError:
            raise

    def screenshot(self, testid):
        '''
        执行测试用例后截图
        :param testid:
        :return:
        '''
        #driver = self.driver
        filedir = os.path.abspath('img')
        img_name = testid + '.png'
        img_filepath = filedir + '/' + img_name
        self.driver.get_screenshot_as_file(img_filepath)
        return img_name

if __name__ == '__main__':
    print(set_element_dict('Menu', 'PersonalCenter'))
