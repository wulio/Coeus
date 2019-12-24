# coding: utf-8
from utils.manager import Manager

__author__ = 'deff'
import sys

if len(sys.argv) < 1:
    print("usage:python  coeus.py sdk_path [-d]")
    print("-d means delete temp file.")
    sys.exit(0)

sdk_path = sys.argv[1]
# test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test")
# sdk_path = os.path.join(test_path,"getui_2.13.3.0-gisdk_3.1.9.1-gssdk_2.3.0.0.aar")

m = Manager(sdk_path)
m.start()

if len(sys.argv) > 2 and sys.argv[2] == "-d":
    m.delete()
