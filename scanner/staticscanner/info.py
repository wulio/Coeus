# coding: utf-8
import re
import os

from utils.fileutils import FileUtils
from utils.md5 import Md5
from scanner.base import BaseScanner
from utils.sdkinfo import sdkinfo
from config import config

__author__ = 'deff'


##基础信息,权限,包名
class InfoScanner(BaseScanner):
    def __init__(self):
        super().__init__()

    # 做初始化操作
    def init(self):
        pass

    # 静态扫描
    def scan(self):
        sdkinfo.sdk_md5 = Md5.md5_file(sdkinfo.sdk_path)
        self.get_info()
        self.get_soname()
        self.get_other_libs()

    def get_info(self):
        sdkinfo.sdk_name = os.path.splitext(os.path.basename(sdkinfo.sdk_path))[0]
        sdkinfo.sdk_size = str(int(os.path.getsize(sdkinfo.sdk_path) / 1024))
        if not FileUtils.is_file_exit(config.xml_path):
            return

        with open(config.xml_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.find('package=') > -1:
                    re_name = re.compile(r"package=\"(.*?)\"\s")
                    sdkinfo.package_name = re_name.findall(line)[0]
                if line.find('versionName') > -1:
                    re_version = re.compile(r"versionName=\"(.*?)\"\s")
                    sdkinfo.version_name = re_version.findall(line)[0]
                if line.find('uses-permission') > -1:
                    re_per = re.compile(r"android:name=\"(.*?)\"\s")
                    permission = re_per.findall(line)[0]
                    sdkinfo.permissions.append(permission)
                if line.find('minSdkVersion') > -1:
                    re_min = re.compile(r"android:minSdkVersion=\"(.*?)\"\s")
                    sdkinfo.min_sdk_version = re_min.findall(line)[0]
                if line.find('targetSdkVersion') > -1:
                    re_target = re.compile(r"android:targetSdkVersion=\"(.*?)\"\s")
                    sdkinfo.target_sdk_version = re_target.findall(line)[0]
                if line.find("android:allowBackup") > -1:
                    re_allow = re.compile(r"android:allowBackup=\"(.*?)\"\s")
                    sdkinfo.allow_back_up = re_allow.findall(line)[0].lower() == "true"
                if line.find("android:debuggable") > -1:
                    re_debug = re.compile(r"android:debuggable=\"(.*?)\"\s")
                    sdkinfo.debuggable = re_debug.findall(line)[0].lower() == "true"
    # /jni/abi_name/name.so（其中“abi_name”是 Android 支持的 ABI 之一）
    def get_soname(self):
        if FileUtils.is_file_exit(config.jni_path):
            for dirpath, dirnames, filenames in os.walk(config.unzip_path):
                for filename in filenames:
                    if filename.endswith(".so"):
                        sdkinfo.sdk_soname = filename

    # libs
    def get_other_libs(self):
        if FileUtils.is_file_exit(config.libs_path):
            for home, dir, filenames in os.walk(config.libs_path):
                for filename in filenames:
                    sdkinfo.other_libs.append(filename)

    # /assets/
    def get_assets(self):
        if FileUtils.is_file_exit(config.assets_path):
            for home, dir, filenames in os.walk(config.libs_path):
                for filename in filenames:
                    sdkinfo.assets_files.append(filename)

    # 输出报告,xml格式(方便单独展示)，json格式
    def report(self):
        report = "<sdkinfo>" + \
                 "<sdkname>" + sdkinfo.sdk_name + "</sdkname>" + \
                 "<packageName>" + sdkinfo.package_name + "</packageName>" + \
                 "<version>" + sdkinfo.version_name + "</version>" + \
                 "<sdksize>" + sdkinfo.sdk_size + "KB" + "</sdksize>" + \
                 "<md5>" + sdkinfo.sdk_md5 + "</md5>" + \
                 "<targetsdk>" + "targetSdkVersion " + sdkinfo.target_sdk_version + "</targetsdk>" + \
                 "<minsdk>" + "minSdkVersion " + sdkinfo.min_sdk_version + "</minsdk>"

        for permisson in sdkinfo.permissions:
            report += "<permission>" + permisson + "</permission>"

        report += "</sdkinfo>"
        return report

    # 结束操作
    def delete(self):
        pass

    def __del__(self):
        pass


if __name__ == '__main__':
    sdkinfo.sdk_path = r"E:\work\workPython\sdkscan\test\spartasdk-2.0.0.aar"
    config.xml_path = r"E:\work\workPython\sdkscan\temp\20191223-10-41-40\unzip\AndroidManifest.xml"
    info = InfoScanner()
    info.init()
    info.scan()
    info.report()
