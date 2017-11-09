# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
# Create your tests here.
from pysphere import VIProperty
from pysphere.vi_property import getmembers
from pysphere.resources import VimService_services as VI
from vc.src.conn_vcserver import ConnHelper

c = ConnHelper()
server = c.start_connect_server()
