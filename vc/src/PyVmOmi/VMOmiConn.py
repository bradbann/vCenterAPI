from vc.src import conf
from pyVim.connect import SmartConnect, Disconnect
import ssl

class VMOmiConn(object):
    def __init__(self):
        self.ssl = ssl._create_default_https_context = ssl._create_unverified_context

    def startConn(self):
        try:
            connObj = SmartConnect(host=conf.HOST, user=conf.USER, pwd=conf.PASSWORD)
            return connObj
        except:
            connObj = SmartConnect(host=conf.HOST, user=conf.USER, pwd=conf.PASSWORD, sslContext=self.ssl)
            return connObj
