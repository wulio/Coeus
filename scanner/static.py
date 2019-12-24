# coding: utf-8
from scanner.staticscanner.policy import PolicyScanner
from scanner.base import BaseScanner
from scanner.staticscanner.api import ApiScanner
from scanner.staticscanner.info import InfoScanner

__author__ = 'deff'


# 静态
class StaticScanner(BaseScanner):
    def __init__(self, is_aar):
        super().__init__()
        # 此处可以添加不同的规则扫描器
        self.static_scanners = []
        self.is_aar = is_aar
        self.init()

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

    # 可单独直接开始
    def start(self):
        if self.is_aar:
            self.static_scanners = [InfoScanner(), PolicyScanner(), ApiScanner()]
        else:
            self.static_scanners = [InfoScanner(), ApiScanner()]

        report = ""
        for scanner in self.static_scanners:
            scanner.init_tag()
            scanner.init()
            scanner.scan()
            report += scanner.report()
            scanner.delete()
            scanner.end_tag()

        return report
