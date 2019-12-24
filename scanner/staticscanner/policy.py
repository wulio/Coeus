# coding: utf-8
import linecache
import logging
import os
import json

from scanner.staticscanner.info import InfoScanner
from utils.fileutils import FileUtils
from scanner.base import BaseScanner
from utils.sdkinfo import sdkinfo
from config import config

__author__ = 'deff'


## 政策信息，权限，target api
class PolicyScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.target_sdk = False
        self.so_64 = False
        self.policy = []
        self.permissions_policy = {}

    # 做初始化操作
    def init(self):

        with open(config.POLICY_PERMISSION_PATH, "r", encoding="utf-8") as f:
            self.permissions_policy = json.load(f)

            # 静态扫描

    def scan(self):
        if not FileUtils.is_file_exit(config.POLICY_PERMISSION_PATH):
            logging.error("POLICY_TXT not in.")
            return

        if FileUtils.is_file_exit(config.xml_path):
            self.find_permission_policy()
            if int(sdkinfo.target_sdk_version) < 28:
                self.target_sdk = True
        else:
            logging.info("no xml")

        self.so_policy()

        self.find_api_policy()

    def so_policy(self):
        if FileUtils.is_dir_exit(config.jni_path):
            arm_64 = os.path.join(config.jni_path, "arm64-v8a")
            x86_64 = os.path.join(config.jni_path, "x86_64")
            if not FileUtils.is_dir_exit(arm_64) and not FileUtils.is_dir_exit(x86_64):
                self.so_64 = True
        else:
            if FileUtils.is_dir_exit(config.unzip_path):
                arm_64_2 = os.path.join(config.unzip_path, "arm64-v8a")
                x86_64_2 = os.path.join(config.unzip_path, "x86_64")
                self.so_64 = FileUtils.is_dir_empty(arm_64_2) and FileUtils.is_dir_empty(x86_64_2)

    def find_permission_policy(self):

        for permission in sdkinfo.permissions:
            find_flag = False
            for pe_policy in self.permissions_policy.values():
                if pe_policy["name"] == permission:
                    find_flag = True
                    summary = pe_policy["summary"]
                    desc = pe_policy["desc"]
                    level = pe_policy["level"]
                    if int(level) > 0:
                        p = {
                            "name": permission,
                            "summary": summary,
                            "desc": desc,
                            "level": level
                        }
                        self.policy.append(p)
                    break
            if not find_flag:
                logging.info("permission in policy_permission_json not find:" + permission)
                # print("permission in policy_permission_json not find:" + permission)

    # 检测特殊api
    # 放置apiscanner中处理
    def find_api_policy(self):
        pass

    def get_msg(self, line):
        message = linecache.getline(config.POLICY_PERMISSION_PATH, line)
        return message[(message.find('\"') + 1):message.rfind('\"')]

    # 输出报告
    def report(self):
        report = "<base-policy>"
        if self.target_sdk:
            report += "<target_sdk>" + \
                      "<name>" + sdkinfo.target_sdk_version + "</name>" + \
                      "<summary>" + "当前sdkversoin为" + sdkinfo.target_sdk_version + "</summary>" + \
                      "<desc>" + "电信终端产业协会（TAF）发布的《移动应用软件高 API 等级预置与分发自律公约》要求，截止到2019年5月1日所有新发布的应用 API 必须为26或更高，2019年8月1日现有应用 API 必须升级为26或更高。2019-11-1之后，上架谷歌Play商店要求应用的TargetSdkVersion>=28 " + "</desc>" + \
                      "<level>" + " 2 " + "</level>" + \
                      "<slu>" + "联系sdk开发者，修改sdk版本号" + "</slu>" + \
                      "</target_sdk>"

        if self.so_64:
            report += "<warning-so>" + \
                      "<name>" + "缺少64位so,google上架有要求，国内似乎暂无影响" + "</name>" + \
                      "<summary>" + "存在so但缺乏64位架构" + "</summary>" + \
                      "<desc>" + "目前谷歌要求应用必须支持64位才能上架play商店，OEM厂商为了降低芯片的成本，可能只提供支持64位的版本，不考虑向下兼容。如果应用不适配支持64位，在后面的一些手机上将会无法运行。" + "</desc>" + \
                      "<level>" + " 0 " + "</level>" + \
                      "<slu>" + "联系sdk开发者，修改sdk版本号" + "</slu>" + \
                      "</warning-so>"

        for polic in self.policy:
            report += "<warning-permission>"
            report += "<name>" + polic["name"] + "</name>" + \
                      "<summary>" + polic["summary"] + "</summary>" + \
                      "<desc>" + polic["desc"] + "</desc>" + \
                      "<level>" + polic["level"] + "</level>" + \
                      "<slu>" + " 请仔细查看该sdk用途和说明，如必须该权限需在app中保证用户同意，且隐私数据做匿名化处理,以此符合中央网信办、工信部、公安部、市场监管总局要求。" + "</slu>"
            report += "</warning-permission>"
        report += "</base-policy>"

        return report

    # 结束操作
    def delete(self):
        del self.permissions_policy

    def __del__(self):
        pass


if __name__ == '__main__':
    sdkinfo.sdk_path = r"E:\work\workPython\sdkscan\test\getui_2.13.3.0-gisdk_3.1.9.1-gssdk_2.3.0.0.aar"
    config.xml_path = r"E:\work\workPython\sdkscan\temp\20191223-10-41-40\unzip\AndroidManifest.xml"
    info = InfoScanner()
    info.init()
    info.scan()
    info.report()
    polic = PolicyScanner()
    polic.init()
    polic.scan()
    polic.report()
