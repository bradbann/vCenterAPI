#-*- coding: utf-8 -*-
import os
"""
配置您的center服务器地址、用户名、及密码
"""
HOST = '192.168.1.182'

USER = 'administrator'

PASSWORD = '1qaz@WSX'

#任务ID和虚拟机列表绑定的数据文件
#DTFile = 'C:\VMware\\taskID_vmlist.pk1'
DT_PATH = os.path.dirname(__file__)
DT_FILE_PATH = "{pspath}\\".format(pspath=DT_PATH.replace("/", "\\"))
T = DT_FILE_PATH.split("\\")
DTFile = "%s\\%s\\taskID_vmlist.pk1" % (T[0], T[1])


