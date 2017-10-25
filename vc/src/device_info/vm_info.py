# -*- coding: utf-8 -*-
from vc.src.vm_helper import VMInstance

class VM_Info(VMInstance):
    '''这个类用于获取虚拟机的基础数据'''

    def __init__(self):
        pass

    def get_vm_basic_info(self, vminstance):
        '''获取虚拟机基础信息
        参数:
            vminstance: 虚拟机实例
        '''
        try:
            data_total = []
            for vm in vminstance:
                # 获取磁盘信息
                data = vm['obj']._disks
                disk_list = []
                for i in range(len(data)):
                    vdiskFile = data[i]["files"][0]["name"]
                    vdiskSize = data[i]["capacity"]  # 单位是KB
                    vdiskName = data[i]["label"]
                    vDiskunitNumber = data[i]["device"]["unitNumber"]
                    vdiskData = {"vDiskunitNumber":vDiskunitNumber,"vdiskFile": vdiskFile, "vdiskSize": vdiskSize, "vdiskName":vdiskName}
                    disk_list.append(vdiskData)

                #获取网卡信息
                nic_list = []
                for dev in vm["obj"].properties.config.hardware.device:
                    if dev._type in ["VirtualVmxnet3", "VirtualE1000", "VirtualE1000e", "VirtualPCNet32", "VirtualVmxnet"]:  # 过滤有哪些适配器类型，如有新的类型，需在这里添加
                        nic_data = {"nicType": dev._type, "NetworkConnection": dev._obj.Backing.DeviceName,
                                    "nicName": dev._obj.DeviceInfo.Label, "mac": dev._obj.MacAddress,
                                    "WakeOnLanEnabled": dev._obj.WakeOnLanEnabled
                                    }
                        nic_list.append(nic_data)

                #获取虚拟机快照信息
                snapshots_list = []
                snapshots_instance = vm["obj"].get_snapshots()
                for snapshots_items in snapshots_instance:
                    time_data = snapshots_items.get_create_time()
                    new_time = "%s-%s-%s %s:%s:%s" % (time_data[0],time_data[1],time_data[2],time_data[3],time_data[4],time_data[5])
                    snapshots_data = {
                        "SnapshotsName": snapshots_items.get_name(),
                        "Description": snapshots_items.get_description(),
                        "CreatedTime": new_time,
                        "State": snapshots_items.get_state(),
                        "Path": snapshots_items.get_path(),
                        # "Parent":snapshots_items.get_parent(),
                        # "Children":snapshots_items.get_children()
                    }
                    snapshots_list.append(snapshots_data)

                vm_status = vm["obj"].get_status() #获取电源状态
                esxi_host = vm["obj"].properties.runtime.host.name #获取所承载的物理机
                vmIdent = vm['obj']._mor #获取虚拟机唯一标识
                osType = vm['obj']._properties["guest_full_name"] #获取操作系统类型
                memory_mb_size = vm['obj']._properties["memory_mb"] #获取内存大小，单位MB
                cpuNumber = vm['obj']._properties["num_cpu"] #获取CPU数量

                #获取虚拟机IP地址
                vmip = None
                try:
                    vm["obj"].properties._flush_cache()
                    ip = vm["obj"].properties.guest.ipAddress
                    vmip = ip
                except AttributeError:
                    vmip = "null"

                #数据数据汇总
                data_total.append({"osType":osType,
                                    "ip":vmip,
                                    "vmIdent":vmIdent,
                                    "name": vm["name"],
                                    "vmxfile": vm["path"],
                                    "state": vm_status,
                                    "esxi":esxi_host,
                                    "virtualdisk":disk_list,
                                    "memorySize":memory_mb_size,
                                    "cpuNumber":cpuNumber,
                                    "NIC":nic_list,
                                    "snapshots": snapshots_list
                                    })
            return data_total
        except Exception, e:
            print e
            return False