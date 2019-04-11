# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

import unittest

from context import peakinvestigator

from peakinvestigator.actions import *

class TestSftpAction(unittest.TestCase):

    def setUp(self):
        self.action = SftpAction("4.2", "joe", "badpw", 1234)


    def test_build_query(self):
        query = self.action.build_query()

        self.assertEqual("SFTP", query["Action"])
        self.assertEqual("4.2", query["Version"])
        self.assertEqual("joe", query["User"])
        self.assertEqual("badpw", query["Code"])
        self.assertEqual(1234, query["ID"])


    def test_response(self):
        response = '{"Action":"SFTP", "Host":"peakinvestigator.veritomyx.com", ' + \
                        '"Port":22022, "Directory":"/files", "Login":"Vt504", ' + \
                        '"Password":"0UtnWMvzoi2jF4BQ", ' + \
                        '"Fingerprints":[ ' + \
                        '{"Signature":"DSA","Algorithm":"MD5","Hash":"96:bd:da:62:5a:53:1a:2f:82:87:65:7f:c0:45:71:94"},' + \
                        '{"Signature":"DSA","Algorithm":"SHA256","Hash":"b9SOs40umHMywBa2GtdsOhr/wgP1L6nfXWugjRrJTaM"}, ' + \
                        '{"Signature":"ECDSA","Algorithm":"MD5","Hash":"5c:6f:c7:c7:79:c0:76:90:4d:3a:a1:7a:81:0e:0a:57"}, ' + \
                        '{"Signature":"ECDSA","Algorithm":"SHA256","Hash":"d2HXgeUSmWN+gq+9V7Wad5xWaCxk+mh45F81K951MCU"}, ' + \
                        '{"Signature":"RSA","Algorithm":"MD5","Hash":"d2:be:b8:2e:3c:be:84:e4:a3:0a:c8:42:5c:6b:39:4e"}, ' + \
                        '{"Signature":"RSA","Algorithm":"SHA256","Hash":"QBsg8ejj4gZun4AWd4WBTJw89ftcLR9x/dZoG223srg"}]}'
        self.action.process_response(response)

        self.assertEqual("peakinvestigator.veritomyx.com", self.action.host)
        self.assertEqual(22022, self.action.port)
        self.assertEqual("/files", self.action.directory)
        self.assertEqual("Vt504", self.action.sftp_username)
        self.assertEqual("0UtnWMvzoi2jF4BQ", self.action.sftp_password)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
