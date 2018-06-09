# -*- coding: utf-8 -*-
import unittest
from time import sleep

from commonPac.mydriver import MyDriver
from commonPac.common import Element


class Test001(unittest.TestCase):

    def setUp(self):
        self.driver = MyDriver.get_driver()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        Element('Menu', 'PersonalCenter',self.driver)


