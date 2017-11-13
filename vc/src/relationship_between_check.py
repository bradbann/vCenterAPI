#coding:utf-8
"""Resource relationship checking"""

from vc.src.conn_vcserver import ConnHelper
from vc.src.db.table_ps_datastore_host_relation import readAllData_from_datastore_host_relation

c = ConnHelper()
s = c.start_connect_server()

def datastore_host_relation(datastore_name=None):
    """Find out which physical host you belong to by storing your name
    However, the write database is performed by the ps script get_datastorage_info.ps1
    """
    for dt in readAllData_from_datastore_host_relation():
        if datastore_name == dt["datastore"]:
            return str(dt["esxi"])


