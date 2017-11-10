#coding:utf-8
"""
资源关系检查
"""
from vc.src.conn_vcserver import ConnHelper
from vc.src.db.table_ps_datastore_host_relation import readAllData_from_datastore_host_relation

c = ConnHelper()
s = c.start_connect_server()

def datastore_host_relation(datastore_name=None):
    """通过存储名字检测出属于哪台物理主机
    但写入数据库是由ps脚本get_datastorage_info.ps1操作
    """
    # for datastore_name in s.get_datastores().values():
    #     print datastore_name
    for dt in readAllData_from_datastore_host_relation():
        if datastore_name == dt["datastore"]:
            return str(dt["esxi"])


