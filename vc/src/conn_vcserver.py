#-*- coding: utf-8 -*-

import conf as VC
from pysphere import VIServer
import ssl

class ConnHelper(object):
    """Connect the VCENTER SERVER"""
    def __init__(self):
        """The way pySphere connects to vcenter is to use an HTTPS form of SSL connection, preferably with a vcenter
        encryption certificate.Otherwise, the certificate validation failed, after the code import, if the certificate
        is not correct. Add: SSL. _create_default_https_context = ssl._create_unverified_context is used to set
        SSL unverifiable.
        """
        self.ssl = ssl._create_default_https_context = ssl._create_unverified_context
        self.server = VIServer()

    def start_connect_server(self):
        """The address, username, and password to connect to the VC server are set in conf. Py"""
        try:
            self.server.connect(VC.HOST, VC.USER, VC.PASSWORD)
            return self.server
        except Exception, err:
            print "Cannot connect to host: "+VC.HOST+" error message: "+ err
