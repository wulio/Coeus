# coding: utf-8
__author__ = 'deff'
import os
import os.path
import zipfile

from utils.fileutils import FileUtils


class ZipUtils:
    @staticmethod
    def unzip(file_path, dst_path):
        if not zipfile.is_zipfile(file_path):
            return False

        if not os.path.exists(dst_path):
            os.mkdir(dst_path, 0o777)

        zfobj = zipfile.ZipFile(file_path)
        for name in zfobj.namelist():
            oriname = name
            if os.sep == '\\':
                name = name.replace('/', os.sep)
            if name.endswith(os.sep):
                FileUtils.create_dir(os.path.join(dst_path, name))
                pass
            else:
                filepath = os.path.join(dst_path, name)
                dir = os.path.dirname(filepath)

                if not os.path.exists(dir):
                    FileUtils.create_dir(dir)

                file = open(filepath, 'wb')
                file.write(zfobj.read(oriname))
                file.close()

        return True
