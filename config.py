# coding: utf-8
__author__ = 'deff'

import os


class Config:
    RESULT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "result")
    TEMP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp")  # 工作目录
    TOOL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tools")
    SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "script")
    POLICY_PERMISSION_PATH = os.path.join(SCRIPT_PATH, "policy_permission.json")
    POLICY_API_PATH = os.path.join(SCRIPT_PATH, "policy_api.json")
    EXPLOIT_API_PATH = os.path.join(SCRIPT_PATH, "exploit_api.json")

    def __init__(self):
        self.sdk_path = ""
        self.result_path = ""

        self.temp_path = ""
        self.unzip_path = ""
        self.decompile_path = ""

        self.java_path = ""
        self.smali_path = ""

        self.jar_path = ""
        self.so_path = ""
        self.xml_path = ""
        self.res_path = ""
        self.assets_path = ""
        self.libs_path = ""
        self.jni_path = ""


config = Config()
