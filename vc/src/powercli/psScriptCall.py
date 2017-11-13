#coding:utf-8
"""Powershell script invocation"""

import subprocess
from set_PShell_ScriptFile import *

def callScript_get_port_group():
    '''The call gets the virtual port group data ps script,
    which is written to the database by the powershell'''
    try:
        print "The Virtual Port Group data is being acquired..."
        args = [r"powershell", script_get_port_group]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        dt = p.stdout.read()
        return True
    except Exception,error:
        print error
        return False

def callScript_get_datastorage_info():
    '''The call detects which esxi script belongs to, and the powershell writes the data to the database'''
    try:
        print "getting the data for storing and esxi..."
        args = [r"powershell", script_get_datastorage_info]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        dt = p.stdout.read()
        return True
    except Exception, e:
        print e
        return False