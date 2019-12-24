# coding: utf-8
import logging

__author__ = 'deff'


class BaseScanner:
    def __init__(self):
        pass

    # 做初始化操作
    def init_tag(self):
        logging.info(self.__class__.__name__ + " start.")

    # 静态扫描
    def scan(self):
        pass

    # 输出报告
    def report(self):
        pass

    # 结束操作
    def delete(self):
        pass

    def end_tag(self):
        logging.info(self.__class__.__name__ + " end.")

    # 可单独直接开始
    def start(self):
        pass
