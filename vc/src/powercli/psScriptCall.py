#coding:utf-8
"""powershell脚本调用"""
import subprocess

# 定义ps脚本
__get_port_group_script = r"C:\VMware\vc\src\powercli\psscript\get_port_group.ps1"

def callScript_get_port_group():
    '''调用获取虚拟端口组数据ps脚本'''
    args = [r"powershell", __get_port_group_script]
    subprocess.Popen(args, stdout=subprocess.PIPE)

