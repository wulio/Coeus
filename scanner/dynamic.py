# coding: utf-8
__author__ = 'deff'

from scanner.base import BaseScanner


##动态信息

class DynamicScanner(BaseScanner):
    def __init__(self):
        super().__init__()

    ##可单独直接开始
    def start(self):
        return ""

    # 做初始化操作
    def init(self):
        pass

    # 扫描
    def scan(self):
        pass

    # 输出报告
    def report(self):
        pass

    # 结束操作
    def delete(self):
        pass

    def __del__(self):
        pass
