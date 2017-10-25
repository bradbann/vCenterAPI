#-*- coding: utf-8 -*-
import os

T_PATH = os.path.dirname(__file__)
PS_SCRIPT_PATH = "{pspath}".format(pspath=T_PATH.replace("/", "\\"))

pstests = "%s\pstests.ps1" % (PS_SCRIPT_PATH)
print pstests
