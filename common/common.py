import os
import configparser

curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "./../main.ini")
conf = configparser.RawConfigParser()
conf.read(cfgpath, encoding="utf-8")


def get_first_error(errors):  # 取出序列化抛出错误的一个错误，用于返回给用户
    for key, value in errors.items():
        return key, value
