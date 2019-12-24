# coding: utf-8
import shutil

__author__ = 'deff'

import os


class FileUtils:
    def __init__(self):
        pass

    @staticmethod
    def is_file_exit(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def is_dir_exit(dir_path):
        return os.path.isdir(dir_path) and os.path.exists(dir_path)

    @staticmethod
    def is_dir_empty(dir_path):
        if not FileUtils.is_dir_exit(dir_path):
            return False
        return len(os.listdir(dir_path)) == 0

    # 创建多级目录，比如c:\\test1\\test2,如果test1 test2都不存在，都将被创建
    @staticmethod
    def create_dir(to_create_path):
        dirs = to_create_path.split(os.sep)
        path = ''
        for di in dirs:
            di += os.sep
            path = os.path.join(path, di)
            if not os.path.exists(path):
                os.mkdir(path, 0o777)

    @staticmethod
    def delete_file(to_del_file):
        if os.path.exists(to_del_file):
            os.remove(to_del_file)

    @staticmethod
    def delete_dirs(to_del_dirs):
        if os.path.exists(to_del_dirs):
            shutil.rmtree(to_del_dirs)
