## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

import unittest

from context import peakinvestigator

from peakinvestigator.actions import *


class TestUploadAction(unittest.TestCase):

    def setUp(self):
        self.action = UploadAction("4.2", "joe", "badpw", "1234", "Test")

    def test_build_query(self):
        query = self.action.build_query()

        self.assertEqual("UPLOAD", query["Action"])
        self.assertEqual("4.2", query["Version"])
        self.assertEqual("joe", query["User"])
        self.assertEqual("badpw", query["Code"])
        self.assertEqual("1234", query["ID"])

    def test_response(self):
        response = '{"Action":"UPLOAD", "Host":"peakinvestigator.veritomyx.com", "Port":"22022", "Token": "640f89508eba4d9e8b5951fb083e97ac"}'
        self.action.process_response(response)

        self.assertEqual("peakinvestigator.veritomyx.com", self.action.host)
        self.assertEqual("22022", self.action.port)
        self.assertEqual("640f89508eba4d9e8b5951fb083e97ac", self.action.token)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()