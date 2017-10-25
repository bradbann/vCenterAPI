# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
# Create your tests here.
import json, sys
from vc.src.conn_vcserver import ConnHelper
from vc.src.vm_helper import VMAction, VMInstance
from pysphere.resources import VimService_services as VI
from pysphere import VIProperty
from vc.src.vmExistChecked import vmListExistChecked, aVM_ExistChecked
from vc.src.device_info.vm_info import VM_Info
action = VMInstance()


vm = action.get_vm_instance_by_name("ldvvv_1")
vm = vm[0]
if vm["obj"].is_powered_on():
    print "vm power on..."
else:
    print "vm power off.."


'''
is_blocked_on_msg
is_powered_off
is_powered_on
is_powering_off
is_powering_on
is_resetting
is_reverting
is_suspended
is_suspending
'''

