#coding:utf-8
"""powershell脚本调用"""

import subprocess
import time

# 定义ps脚本
__get_port_group_script = r"C:\VMware\vc\src\powercli\psscript\get_port_group.ps1"

def get_port_group():
    while True:
        print "数据获取：虚拟端口组数据正在获取..."
        args = [r"powershell", __get_port_group_script]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        p.stdout.read()
        print "虚拟端口组数据获取完成..."
        time.sleep(1800)