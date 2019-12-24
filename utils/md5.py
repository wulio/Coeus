# coding: utf-8
__author__ = 'deff'
'''
 md5相关函数
'''
import hashlib


class Md5:
    def __init__(self):
        pass

    @staticmethod
    def md5(words):
        m = hashlib.md5()
        m.update(words.encode(encoding='utf-8'))
        return m.hexdigest().lower()

    @staticmethod
    def md5_file(file_path):
        with open(file_path, mode="rb") as file:
            m = hashlib.md5()
            while True:
                str_read = file.read(1024 * 1024)
                if not str_read:
                    break
                m.update(str_read)
            return m.hexdigest().lower()


if __name__ == "__main__":
    pass
    # print(Md5.md5(u"test"))
    # print(Md5.md5_file(u"d:\\test.txt"))
