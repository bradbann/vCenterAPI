#coding:utf-8
from pysphere import VIServer
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask
from vc.src.conf import HOST, USER, PASSWORD
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from pysphere import VIServer, VITask
from pysphere.resources import VimService_services as VI

server = VIServer()
server.connect(HOST, USER, PASSWORD)

vm = "aaa"
label = "br-int" #nic to remove

vm_obj = server.get_vm_by_name(vm)
if not vm_obj:
    raise Exception("VM %s not found" % vm)

net_device = None
for dev in vm_obj.properties.config.hardware.device:
    if (dev._type in ["VirtualE1000", "VirtualE1000e",
                     "VirtualPCNet32", "VirtualVmxnet"]
    and hasattr(dev, "backing") and hasattr(dev.backing, "deviceName")
    and dev.backing.deviceName == label):
        net_device = dev._obj
        break
if not net_device:
    raise Exception("NIC not found")

request = VI.ReconfigVM_TaskRequestMsg()
_this = request.new__this(vm_obj._mor)
_this.set_attribute_type(vm_obj._mor.get_attribute_type())
request.set_element__this(_this)
spec = request.new_spec()
dev_change = spec.new_deviceChange()
dev_change.set_element_operation("remove")
dev_change.set_element_device(net_device)

spec.set_element_deviceChange([dev_change])
request.set_element_spec(spec)
ret = server._proxy.ReconfigVM_Task(request)._returnval

#Wait for the task to finish
task = VITask(ret, server)
status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
if status == task.STATE_SUCCESS:
    print "VM %s successfully reconfigured" % vm
elif status == task.STATE_ERROR:
    print "Error reconfiguring vm: %s" % vm, task.get_error_message()

server.disconnect()