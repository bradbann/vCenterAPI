#coding:utf-8
from pysphere import *
from pysphere.resources import VimService_services as VI
from vc.src.conn_vcserver import ConnHelper

class NIC:
    _conn = ConnHelper()
    def __init__(self):
        self.s = self._conn.start_connect_server()

    def nic_chage_conn(self, vminstance, nic_name, network_label):
        nic_name = nic_name
        network_label = network_label
        vm_obj = vminstance
        if not vm_obj:
            raise Exception("VM not found")

        # Find Virtual Nic device
        net_device = None
        for dev in vm_obj.properties.config.hardware.device:
            if dev._type in [nic_name]:
                net_device = dev._obj
                break
        if not net_device:
            raise Exception("The vm seems to lack a Virtual Nic")
        net_device.Backing.set_element_deviceName(network_label)

        # Invoke ReconfigVM_Task
        request = VI.ReconfigVM_TaskRequestMsg()
        _this = request.new__this(vm_obj._mor)
        _this.set_attribute_type(vm_obj._mor.get_attribute_type())
        request.set_element__this(_this)
        spec = request.new_spec()
        dev_change = spec.new_deviceChange()
        dev_change.set_element_device(net_device)
        dev_change.set_element_operation("edit")
        spec.set_element_deviceChange([dev_change])
        request.set_element_spec(spec)
        ret = self.s._proxy.ReconfigVM_Task(request)._returnval

        # Wait for the task to finish
        task = VITask(ret, self.s)
        status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
        if status == task.STATE_SUCCESS:
            print "VM successfully reconfigured"
            return True

        elif status == task.STATE_ERROR:
            print "Error reconfiguring"
            return False

    def add_nic(self, vminstance, network_label):
        vm_obj = vminstance
        if not vm_obj:
            raise Exception("VM not found")

        # Invoke ReconfigVM_Task
        request = VI.ReconfigVM_TaskRequestMsg()
        _this = request.new__this(vm_obj._mor)
        _this.set_attribute_type(vm_obj._mor.get_attribute_type())
        request.set_element__this(_this)
        spec = request.new_spec()

        # add a NIC. the network Name must be set as the device name.
        dev_change = spec.new_deviceChange()
        dev_change.set_element_operation("add")
        nic_ctlr = VI.ns0.VirtualPCNet32_Def("nic_ctlr").pyclass()
        nic_backing = VI.ns0.VirtualEthernetCardNetworkBackingInfo_Def("nic_backing").pyclass()
        nic_backing.set_element_deviceName(network_label)
        nic_ctlr.set_element_addressType("generated")
        nic_ctlr.set_element_backing(nic_backing)
        nic_ctlr.set_element_key(4)
        dev_change.set_element_device(nic_ctlr)

        spec.set_element_deviceChange([dev_change])
        request.set_element_spec(spec)
        ret = self.s._proxy.ReconfigVM_Task(request)._returnval

        # Wait for the task to finish
        task = VITask(ret, self.s)
        status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
        if status == task.STATE_SUCCESS:
            print "VM successfully reconfigured"
            return True
        elif status == task.STATE_ERROR:
            print "Error reconfiguring"
            return False