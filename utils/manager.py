# coding: utf-8
import os
import shutil
import subprocess
import logging
import time
import zipfile

from config import config
from scanner.dynamic import DynamicScanner
from scanner.static import StaticScanner
from utils.sdkinfo import sdkinfo
from utils.ziputils import ZipUtils
from utils.fileutils import FileUtils

__author__ = 'deff'


class Manager:
    def __init__(self, sdk_path):

        self.sdk_path = sdk_path
        # 时间命名
        self.result_dir_name = time.strftime("%Y%m%d-%H-%M-%S")
        # 初始化地址和log
        self._init_path()
        self._init_log()
        self.report = ""

    def start(self):
        # 准备工作，解压反编译
        logging.info("start sdk scan..")
        if not FileUtils.is_file_exit(self.sdk_path):
            logging.error("sdk文件不存在")
            return
        pix = os.path.splitext(self.sdk_path)[1]

        if not pix == '.aar' and not pix == '.jar':
            logging.error("sdk文件格式错误")
            return

        sdkinfo.sdk_path = self.sdk_path

        is_aar = pix == '.aar'
        if is_aar:
            logging.info("start unzip..")
            if not ZipUtils.unzip(sdkinfo.sdk_path, config.unzip_path):
                logging.error("unzip error")
                return

            config.jar_path = os.path.join(config.unzip_path, "classes.jar")
            config.res_path = os.path.join(config.unzip_path, "res")
            config.xml_path = os.path.join(config.unzip_path, "AndroidManifest.xml")
            config.jni_path = os.path.join(config.unzip_path, "jni")
            config.assets_path = os.path.join(config.unzip_path, "assets")
            config.libs_path = os.path.join(config.unzip_path, "libs")

            if not FileUtils.is_file_exit(config.jar_path) or not FileUtils.is_file_exit(config.xml_path):
                logging.info("unzip fail,no jar or xml file.")
                return
            logging.info("unzip success.")
        else:
            config.jar_path = os.path.join(config.unzip_path, "classes.jar")
            shutil.copy(config.sdk_path, config.jar_path)

        logging.info("start decompile java.")
        count = self.get_class_file(config.jar_path)
        if self.cfr_decompile(config.jar_path, count):
            logging.info("decompile java success.")
        else:
            logging.info("decompile java error.")

        logging.info("start decompile smali.")
        if self.smali_decompile(config.jar_path):
            logging.info("decompile smali success.")
        else:
            logging.info("decompile smali error.")

        self.scan(is_aar)

    def scan(self, is_aar):
        scanners = [StaticScanner(is_aar), DynamicScanner()]
        logging.info("start scan..")
        self.report = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<sdkscan>\n"
        for scanner in scanners:
            self.report += scanner.start()
        self.report += "</sdkscan>"
        self.save_report()

    def save_report(self):
        config.report_path = os.path.join(config.result_path, "report.xml")
        with open(config.report_path, 'w', encoding='utf-8') as f:
            f.write(self.report)
        logging.info("scan success.")

    # 获取jar中类文件数
    def get_class_file(self, jar_path):
        zf = zipfile.ZipFile(jar_path)
        total_files = len(zf.namelist())
        logging.info("totalfiles:%s" % total_files)
        count = 0
        for s in zf.namelist():
            if (".class" in s) and ("$" not in s):
                count += 1
        return count

    # java,默认输入的文件为标准格式
    def cfr_decompile(self, jar_path, count):
        cfr_path = os.path.join(config.TOOL_PATH, "cfr_0_96.jar")

        starttime = time.time()
        counter = 0
        process = subprocess.Popen(["java", "-jar", cfr_path, jar_path, "--outputdir", config.java_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            if (time.time() - starttime) < 2000:
                line = process.stdout.readline()
                if not line:
                    return True
                if str.encode("Processing") in line:
                    counter += 1
            else:
                subprocess.Popen.kill(process)
                logging.warning(u"超时停止转换，本次仅转换百分之%d.尝试重新转换" % (round(counter * 100 / count)))
                break
        return False

    # smali jar->dex->smali
    def smali_decompile(self, jar_path):
        dx_path = os.path.join(config.TOOL_PATH, "dx.jar")
        dex_path = os.path.join(config.unzip_path, "classes.dex")
        baksmali_jar_path = os.path.join(config.TOOL_PATH, "baksmali.jar")

        process = subprocess.Popen(["java", "-jar", dx_path, "--dex", "--output", dex_path, jar_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.communicate()

        if FileUtils.is_file_exit(dex_path):
            try:
                command = 'java -jar \"%s\" -o \"%s\" \"%s\"' % (baksmali_jar_path, config.smali_path, dex_path)
                p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     shell=True)
                ret = p.communicate()
                if FileUtils.is_dir_empty(config.smali_path):
                    logging.error(u"反编译smali失败")
                    return False
            except Exception as e:
                logging.error(u"反编译smali失败，原因：%s", e)
                return False

        return True

    def _init_path(self):
        config.sdk_path = self.sdk_path
        config.result_path = os.path.join(config.RESULT_PATH, self.result_dir_name)
        config.temp_path = os.path.join(config.TEMP_PATH, self.result_dir_name)

        config.unzip_path = os.path.join(config.temp_path, "unzip")
        config.decompile_path = os.path.join(config.temp_path, "decompile")
        config.java_path = os.path.join(config.decompile_path, "java")
        config.smali_path = os.path.join(config.decompile_path, "smali")

        if not os.path.exists(config.result_path):
            os.mkdir(config.result_path, 0o777)

        if not os.path.exists(config.temp_path):
            os.mkdir(config.temp_path, 0o777)

        if not os.path.exists(config.decompile_path):
            os.mkdir(config.decompile_path, 0o777)

        if not os.path.exists(config.unzip_path):
            os.mkdir(config.unzip_path, 0o777)

    def _init_log(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=r'%s%s%s.log' % (
                                config.result_path, os.sep, "info"),
                            filemode='a')
        #################################################################################################
        # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        ################################################################################################

    # 清空temp目录，可选
    def delete(self):
        FileUtils.delete_dirs(config.temp_path)


if __name__ == '__main__':
    pass
