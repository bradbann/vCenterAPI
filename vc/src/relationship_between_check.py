#coding:utf-8
"""
资源关系检查
"""
from vc.src.conn_vcserver import ConnHelper
from vc.src.powercli.psScriptCall import callScript_get_datastorage_info

class RelationshipBetweenCheck():
    c = ConnHelper()
    s = c.start_connect_server()

    def datastore_host_relation(self):
        """通过存储名字检测出属于哪台物理主机
        但写入数据库是由ps脚本get_datastorage_info.ps1操作
        """
        for datastore_name in self.s.get_datastores().values():
            print datastore_name

a = RelationshipBetweenCheck()
a.datastore_host_relation()
