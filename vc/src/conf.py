#-*- coding: utf-8 -*-
import os
from VMware.settings import BASE_DIR
"""
配置您的center服务器地址、用户名、及密码
"""
HOST = '192.168.1.182'

USER = 'administrator'

PASSWORD = '1qaz@WSX'

#任务ID和虚拟机列表绑定的数据文件
DTFile = os.path.join(BASE_DIR, 'taskID_vmlist.pk1')
