#coding:utf-8
import os

# 定义ps脚本
BASE_DIR = "%s\psscript" % (os.path.split(os.path.realpath(__file__))[0])

def file_Generated(base_dir, filename):
    f = r"%s" % (filename)
    script_file = os.path.join(base_dir, f)
    return script_file

script_get_port_group = file_Generated(BASE_DIR, "get_port_group.ps1")
script_get_datastorage_info = file_Generated(BASE_DIR, "get_datastorage_info.ps1")


