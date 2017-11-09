#coding:utf-8
"""powershell脚本调用"""
import subprocess
from set_PShell_ScriptFile import *

def callScript_get_port_group():
    '''调用获取虚拟端口组数据ps脚本'''
    try:
        print "正在获取Virtual Port Group数据..."
        args = [r"powershell", script_get_port_group]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        dt = p.stdout.read()
        return True
    except Exception,error:
        print error
        return False

def callScript_get_datastorage_info(datastore_name):
    # 通过datastore name 检测属于哪台esxi主机
    try:
        args = [r"powershell", script_get_datastorage_info,datastore_name]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        dt = p.stdout.read()
        return True
    except Exception, e:
        print e
        return False
