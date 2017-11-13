# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
# Create your tests here.
from pysphere import VIProperty
from pysphere.vi_property import getmembers
from pysphere.resources import VimService_services as VI
from vc.src.conn_vcserver import ConnHelper

# c = ConnHelper()
# server = c.start_connect_server()

from pyVim import connect
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
si = connect.SmartConnect(host="192.168.1.182", user="administrator", pwd="1qaz@WSX")
esxi = si.content.searchIndex.FindByDnsName(None, '192.168.1.189', False)
