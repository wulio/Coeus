# coding: utf-8
__author__ = 'deff'


class SdkInfo:
    def __init__(self):
        self.sdk_name = ""
        self.sdk_size = ""
        self.sdk_path = ""
        self.sdk_md5 = ""
        self.sdk_soname = ""
        # 其他三方库包
        self.sdk_other_libs = []
        self.assets_files = []
        self.other_libs = []
        self.package_name = ""
        self.version_name = ""
        self.permissions = []
        self.target_sdk_version = ""
        self.min_sdk_version = ""


sdkinfo = SdkInfo()
