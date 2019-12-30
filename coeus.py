# coding: utf-8
from utils.manager import Manager

__author__ = 'deff'
import sys
import os
if len(sys.argv) < 1:
    print("usage:python  coeus.py sdk_path [-d]")
    print("-d means delete temp file.")
    print("sdk_path: aar or jar or apk")
    sys.exit(0)


sdk_path = sys.argv[1]

if not os.path.exists(sdk_path):
    sdk_path = os.path.join(os.curdir, sdk_path)
    if not os.path.exists(sdk_path):
        print("please input correct sdk_path.")
        sys.exit(0)

m = Manager(sdk_path)
m.start()

if len(sys.argv) > 2 and sys.argv[2] == "-d":
    m.delete()
