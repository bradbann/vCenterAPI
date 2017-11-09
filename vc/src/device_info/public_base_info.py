#coding:utf-8
from pysphere import MORTypes, VIProperty
from vc.src.conn_vcserver import ConnHelper
from vc.src.db.table_ps_netlabel import readData_from_table_ps_netlabel

class BaseInfo:
    _conn = ConnHelper()
    _baseData = []
    def __init__(self):
        self.s = self._conn.start_connect_server()

    def __get_esxi_host(self):
        '''获取esxi host'''
        esxi_list = []
        for ds_mor, name in self.s.get_hosts().items():
            props = VIProperty(self.s, ds_mor)
            powerState = props.runtime.powerState  # power status
            date = props.runtime.bootTime  # boot time
            bootTime = "%s-%s-%s %s:%s:%s" % (date[0], date[1], date[2], date[3], date[4], date[5])
            props._flush_cache()
            cpuUsage = props.summary.quickStats.overallCpuUsage  # get esxi cpu Usage
            MemoryUsage = props.summary.quickStats.overallMemoryUsage
            CpuCores = props.hardware.cpuInfo.numCpuCores
            MemorySize = props.hardware.memorySize
            dt = {"HostID": ds_mor, "HostName": name, "powerState":powerState, "bootTime":bootTime, "cpuUsage":cpuUsage,
                  "MemoryUsage":MemoryUsage,"CpuCores":CpuCores,"MemorySize":MemorySize
                  }
            esxi_list.append(dt)
        dd = {"Esxi": esxi_list}
        self._baseData.append(dd)

    def __get_cluster(self):
        '''获取集群'''
        clusterid = self.s.get_clusters().keys()
        clustername = self.s.get_clusters().values()
        cls_list = []
        for i in range(len(clusterid)):
            dt = {"ClusterID":clusterid[i], "ClusterName":clustername[i]}
            cls_list.append(dt)
        dd = {"Cluster":cls_list}
        self._baseData.append(dd)

    def __get_datacenter(self):
        '''获取数据中心'''
        datacenterid = self.s.get_datacenters().keys()
        datacentername = self.s.get_datacenters().values()
        data_center_list = []
        for i in range(len(datacenterid)):
            dt = {"DatacenterID":datacenterid[i], "DatacenterName":datacentername[i]}
            data_center_list.append(dt)
        dd = {"Datacenter":data_center_list}
        self._baseData.append(dd)

    def __get_datastore(self):
        '''获取datastore'''
        datastore_list = []
        for ds_mor, name in self.s.get_datastores().items():
            props = VIProperty(self.s, ds_mor)
            Capacity = props.summary.capacity / 1024 / 1024 / 1024
            FreeSpace = props.summary.freeSpace / 1024 / 1024 / 1024
            dt = {"DatastoreID": ds_mor, "DatastoreName": name, "Capacity": Capacity, "FreeSpace": FreeSpace}
            datastore_list.append(dt)
        dd = {"Datastore":datastore_list}
        self._baseData.append(dd)

    def __get_resource_pool(self):
        '''获取资源池'''
        rpid = self.s.get_resource_pools().keys()
        rpname = self.s.get_resource_pools().values()
        if len(rpid) == 0 or len(rpname) == 0:
            print "rpid,rpname not data..."

        rplist = []
        for i in range(len(rpid)):
            dt = {"ResourceID":rpid[i], "ResourceName":rpname[i]}
            rplist.append(dt)
        dd = {"ResourcePool":rplist}
        self._baseData.append(dd)

    def __get_vm_templates(self):
        '''获取虚拟机模板'''
        props = self.s._retrieve_properties_traversal(
            property_names=['name', 'config.template'],
            from_node=None, obj_type=MORTypes.VirtualMachine)
        templates_list = []
        for p in props:
            name = ""
            is_template = False
            for item in p.PropSet:
                if item.Name == "name":
                    name = item.Val
                elif item.Name == "config.template":
                    is_template = item.Val
            if is_template:
                templates_list.append(name)
        dt = {"Templates":templates_list}
        self._baseData.append(dt)

    def __get_network_label(self):
        '''获取网络标签'''
        #network_label = ["br-int", "br-vlan", "public", "VM Network"]
        network_label = readData_from_table_ps_netlabel()
        dt = {"networkLabel":network_label}
        self._baseData.append(dt)

    def main_base_data(self):
        self.__get_esxi_host()
        self.__get_cluster()
        self.__get_datacenter()
        self.__get_datastore()
        self.__get_resource_pool()
        self.__get_vm_templates()
        self.__get_network_label()
        return self._baseData

    def del_baseData_List(self):
        self._baseData = []


