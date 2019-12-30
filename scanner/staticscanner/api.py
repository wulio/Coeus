# coding: utf-8
import os
import re

from utils.tool import Tools

__author__ = 'deff'

from scanner.base import BaseScanner
import json
from utils.sdkinfo import sdkinfo
from config import config


# api审计
# 0. 隐私信息api :手机号/imei/imsi/mac/android id/gps/通讯录/应用程序列表/网页浏览记录(静态检测，后续动态可以进行hook对应函数检测)
# 0.1 http url链接检测
# 1. 调用非SDK接口，带来兼容性问题。(原理一致)https://developer.android.google.cn/distribute/best-practices/develop/restrictions-non-sdk-interfaces
# 2. 存在安全漏洞

# jar -> dex -> smali
# jar -> java (java备份，后续做函数逻辑处理）
# 本打算用jieba或用gensim来匹配，目前简单粗暴正则即可
# 缓存-一个文件一个文件扫-添加-输出报告
class ApiScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.policy_api = {}
        self.exploit_api = {}

        self.report_policy_list = []
        self.report_exploit_list = []
        self.report_url_http = []

    # 做初始化操作
    def init(self):
        with open(config.POLICY_API_PATH, 'r', encoding="utf-8") as f:
            self.policy_api = json.load(f)

        with open(config.EXPLOIT_API_PATH, 'r', encoding="utf-8") as f2:
            self.exploit_api = json.load(f2)

    # 静态扫描
    def scan(self):
        for root, dirs, files in os.walk(config.smali_path):
            for file_name in files:
                if str(file_name).endswith(".smali"):
                    file_path = os.path.join(root, file_name)
                    class_name = file_path.split(config.smali_path)[1]
                    with open(file_path, 'r', encoding="utf-8") as smali_f:
                        lines = smali_f.readlines()
                        for line in lines:
                            line = line.strip()
                            if line.find('http:') > -1 or line.find('https:') > -1:
                                self.gethttp(file_path)
                            self._in_file_(line, class_name)

    def gethttp(self, file_path):
        java_path = file_path.replace("smali", "java")
        if os.path.exists(java_path):
            with open(java_path, 'r', encoding="utf-8") as java_f:
                lines = java_f.readlines()
                for line in lines:
                    line = line.strip()
                    if line.find("http:") < 0 and line.find("https:") < 0:
                        continue
                    urls = self.getmsg(line)
                    for url in urls:
                        if url not in self.report_url_http:
                            self.report_url_http.append(url)

    # 正则搞定
    def getmsg(self, line):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        url = re.findall(pattern, line)
        return url

    def _in_file_(self, line, class_name):
        for p_a in self.policy_api:
            for smalicode in p_a["smalicode"].values():
                if line.find(smalicode) > -1:
                    flag = False
                    for r in self.report_policy_list:
                        if r["name"] == p_a["name"]:
                            flag = True
                            r["classname"].append(class_name)
                            r["smalicode"].append(line)

                    if not flag:
                        classn = [class_name]
                        sn = [line]
                        pa_report = {
                            "name": p_a["name"],
                            "summary": p_a["summary"],
                            "desc": p_a["desc"],
                            "smalicode": sn,
                            "classname": classn,
                            "level": p_a["level"],
                            "sol": p_a["sol"],
                        }
                        self.report_policy_list.append(pa_report)

        for e_a in self.exploit_api:
            if line.find(e_a["smalicode"]) > -1:
                flag = False
                for r in self.report_exploit_list:
                    if r["name"] == e_a["name"]:
                        flag = True
                        r["classname"].append(class_name)
                        r["smalicode"].append(line)

                if not flag:
                    classn = [class_name]
                    sn = [line]
                    ea_report = {
                        "name": e_a["name"],
                        "summary": e_a["summary"],
                        "desc": e_a["desc"],
                        "smalicode": sn,
                        "classname": classn,
                        "level": e_a["level"],
                        "slu": e_a["sol"],
                    }
                    self.report_exploit_list.append(ea_report)

    # 输出报告
    def report(self):
        report = "<api-policy>"
        for report_policy in self.report_policy_list:
            report += "<api>" + "<name>" + report_policy["name"] + "</name>" + \
                      "<summary>" + report_policy["summary"] + "</summary>" + \
                      "<desc>" + report_policy["desc"] + "</desc>"
            for sm in report_policy["smalicode"]:
                report += "<code>" + Tools.xml_assent(sm) + "</code>"

            for cm in report_policy["classname"]:
                report += "<classname>" + cm + "</classname>"

            report += "<level>" + report_policy["level"] + "</level>" + \
                      "<slu>" + report_policy["sol"] + "</slu>" + \
                      "</api>"
        report += "</api-policy>"

        report += "<api-exploit>"
        if sdkinfo.allow_back_up:
            report += "<allowed>" + \
                      "<desc>" + "allowBackup标志为true" + "</desc>" + \
                      "<slu>" + "请将allowBackup设定为false，存在非法备份泄露等安全风险。" + "</slu>" + \
                      "</allowed>"
        if sdkinfo.debuggable:
            report += "<debuggable>" + \
                      "<desc>" + "debuggable标志为true" + "</desc>" + \
                      "<slu>" + "请将debuggable设定为false，存在非法调试等安全风险。" + "</slu>" + \
                      "</debuggable>"

        for report_exploit in self.report_exploit_list:
            report += "<api>" + "<name>" + report_exploit["name"] + "</name>" + \
                      "<summary>" + report_exploit["summary"] + "</summary>" + \
                      "<desc>" + report_exploit["desc"] + "</desc>"

            for sm in report_exploit["smalicode"]:
                report += "<code>" + Tools.xml_assent(sm) + "</code>"

            for cm in report_exploit["classname"]:
                report += "<classname>" + cm + "</classname>"

            report += "<level>" + report_exploit["level"] + "</level>" + \
                      "<slu>" + report_exploit["slu"] + "</slu>" + \
                      "</api>"
        report += "</api-exploit>"

        report += "<url-safe>"
        for url in self.report_url_http:
            report += "<http-code>" + Tools.xml_assent(url) + "</http-code>"
        report += "</url-safe>"
        return report

    # 结束操作
    def delete(self):
        del self.report_policy_list
        del self.report_exploit_list
        del self.policy_api
        del self.exploit_api

    def __del__(self):
        pass


if __name__ == '__main__':
    sdkinfo.sdk_path = r"E:\work\workPython\sdkscan\test\getui_2.13.3.0-gisdk_3.1.9.1-gssdk_2.3.0.0.aar"
    config.smali_path = r"E:\work\workPython\sdkscan\temp\20191223-21-14-19\decompile\smali"
    info = ApiScanner()
    info.init()
    info.scan()
    info.report()
