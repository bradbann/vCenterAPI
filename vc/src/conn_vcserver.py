#-*- coding: utf-8 -*-
"""连接VCENTER SERVER"""

import conf as VC
from pysphere import VIServer
import ssl

class ConnHelper(object):
    """这个类是用于连接center，可被其它类继承使用"""
    def __init__(self):
        """pySphere连接vcenter的方式是使用https形式的ssl连接，最好先安装vcenter的加密证书.
        否则会报错（certificate validation failed）如果安装证书后还报错，那么在代码import之后.
        加一句：ssl._create_default_https_context = ssl._create_unverified_context 这句话的作用是设置ssl不验证.
        """
        self.ssl = ssl._create_default_https_context = ssl._create_unverified_context
        self.server = VIServer()

    def start_connect_server(self):
        """连接VC服务器的地址、用户名和密码在conf.py中设置"""
        try:
            self.server.connect(VC.HOST, VC.USER, VC.PASSWORD)
            return self.server
        except Exception, err:
            print "Cannot connect to host: "+VC.HOST+" error message: "+ err
