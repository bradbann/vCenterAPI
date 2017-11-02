#-*- coding: utf-8 -*-
from pysphere import VITask
from pysphere.resources import VimService_services as VI
from vc.src.conn_vcserver import ConnHelper
import sys

class VDisk():
    '''这个类主要是关于虚拟磁盘的操作:添加磁盘;修改磁盘大小;'''
    _conn = ConnHelper()
    def __init__(self):
        self.s = self._conn.start_connect_server()

    def add_vdisk(self, vminstance, datastore_name, vdisk_size_gb):
        '''添加磁盘'''
        vdisk_size_kb = vdisk_size_gb * 1024 * 1024
        vm = vminstance
        # 虚拟设备节点号码
        Unit_Number = ""
        Temp_Number = 1
        # find the device to be removed
        while True:
            dev = [dev for dev in vm.properties.config.hardware.device
                   if dev._type == "VirtualDisk" and dev.unitNumber == Temp_Number]
            if len(dev) == 0:
                Unit_Number = Temp_Number
                break
            else:
                Temp_Number += 1
                continue

        request = VI.ReconfigVM_TaskRequestMsg()
        _this = request.new__this(vm._mor)
        _this.set_attribute_type(vm._mor.get_attribute_type())
        request.set_element__this(_this)

        spec = request.new_spec()

        dc = spec.new_deviceChange()
        dc.Operation = "add"
        dc.FileOperation = "create"

        hd = VI.ns0.VirtualDisk_Def("hd").pyclass()
        hd.Key = -100
        hd.UnitNumber = Unit_Number
        hd.CapacityInKB = vdisk_size_kb
        hd.ControllerKey = 1000
        backing = VI.ns0.VirtualDiskFlatVer2BackingInfo_Def("backing").pyclass()
        backing.FileName = "[%s]" % datastore_name
        backing.DiskMode = "persistent"
        backing.Split = False
        backing.WriteThrough = False
        backing.ThinProvisioned = False
        backing.EagerlyScrub = False
        hd.Backing = backing
        dc.Device = hd
        spec.DeviceChange = [dc]
        request.Spec = spec
        task = self.s._proxy.ReconfigVM_Task(request)._returnval
        vi_task = VITask(task, self.s)
        # Wait for task to finis
        status = vi_task.wait_for_state([vi_task.STATE_SUCCESS, vi_task.STATE_ERROR])
        if status == vi_task.STATE_ERROR:
            print "ERROR: %s" % (vi_task.STATE_ERROR)
            return False
        else:
            return True
        self.s.disconnect()

    def change_vdisk_size(self, vminstance, vdisk_name, vdisk_size):
        '''修改虚拟磁盘容量大小'''
        vdisk_name_str = vdisk_name.encode('utf-8') # 对磁盘名称进行解码（网络传输过来的值是unicode编码标准），否则将设置失败
        vm_obj = vminstance
        size_kb = int(vdisk_size) * 1024 * 1024 #GB转换为KB
        sizes = {}
        sizes[vdisk_name_str] = size_kb
        print sizes
        hd_sizes_kb = sizes
        hd_to_modify = []
        for dev in vm_obj.properties.config.hardware.device:
            if dev._type == "VirtualDisk" and dev.deviceInfo.label in hd_sizes_kb:
                dev_obj = dev._obj
                dev_obj.set_element_capacityInKB(hd_sizes_kb[dev.deviceInfo.label])
                hd_to_modify.append(dev_obj)

        request = VI.ReconfigVM_TaskRequestMsg()
        _this = request.new__this(vm_obj._mor)
        _this.set_attribute_type(vm_obj._mor.get_attribute_type())
        request.set_element__this(_this)
        spec = request.new_spec()

        # Change the HDs sizes
        dev_changes = []
        for hd in hd_to_modify:
            dev_change = spec.new_deviceChange()
            dev_change.set_element_operation("edit")
            dev_change.set_element_device(hd)
            dev_changes.append(dev_change)
        if dev_changes:
            spec.set_element_deviceChange(dev_changes)

        request.set_element_spec(spec)
        ret = self.s._proxy.ReconfigVM_Task(request)._returnval

        # Wait for the task to finish
        task = VITask(ret, self.s)
        status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
        if status == task.STATE_SUCCESS:
            print "VM successfully reconfigured"
            return True
        elif status == task.STATE_ERROR:
            print "Error reconfiguring vm: %s" % task.get_error_message()
            return False
        self.s.disconnect()

    def delete_vdisk(self, vminstance, unit_number):
        '''删除虚拟机的硬盘
        :parameter
            @vvminstance: 虚拟机实例
            @unit_number: 硬盘ID
        :returns
            pass
        '''
        UNIT_NUMBER = unit_number  # Virtual disk unit number
        vm = vminstance
        # find the device to be removed
        dev = [dev for dev in vm.properties.config.hardware.device
               if dev._type == "VirtualDisk" and dev.unitNumber == UNIT_NUMBER]
        if not dev:
            raise Exception("NO DEVICE FOUND")
        dev = dev[0]._obj
        request = VI.ReconfigVM_TaskRequestMsg()
        _this = request.new__this(vm._mor)
        _this.set_attribute_type(vm._mor.get_attribute_type())
        request.set_element__this(_this)

        spec = request.new_spec()
        dc = spec.new_deviceChange()
        dc.Operation = "remove"
        dc.Device = dev

        spec.DeviceChange = [dc]
        request.Spec = spec

        task = self.s._proxy.ReconfigVM_Task(request)._returnval
        vi_task = VITask(task, self.s)

        status = vi_task.wait_for_state([vi_task.STATE_SUCCESS, vi_task.STATE_ERROR])
        if status == vi_task.STATE_ERROR:
            print "Error removing hdd from vm:", vi_task.get_error_message()
            sys.exit(1)
            return False
        else:
            print "Hard drive successfully removed"
            return True

