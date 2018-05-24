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

class TestPiVersionsAction(unittest.TestCase):

    def setUp(self):
        self.action = PiVersionsAction("4.2", "joe", "badpw")


    def test_build_query(self):
        query = self.action.build_query()
        
        self.assertIn("Version", query)
        self.assertEqual("4.2", query["Version"])
        
        self.assertIn("User", query)
        self.assertEqual("joe", query["User"])

        self.assertIn("Code", query)
        self.assertEqual("badpw", query["Code"])
        
        self.assertIn("Action", query)
        self.assertEqual("PI_VERSIONS", query["Action"])


    def test_response(self):
        response = '{"Action":"PI_VERSIONS", "Current":"1.2", "LastUsed":"", "Count":2, "Versions":["1.2", "1.0.0"]}'
        self.action.process_response(response)
        
        self.assertEqual(self.action.current_version, "1.2")
        self.assertEqual(self.action.last_used, "")
        self.assertEqual(self.action.count, 2)
        self.assertListEqual(self.action.versions, ["1.2", "1.0.0"])
        self.assertIsNone(self.action.error)
        

    def test_error(self):
        response = '{"Action":"PI_VERSIONS", "Error":3, "Message":"Invalid username or password - can not validate"}'
        self.action.process_response(response)
        
        self.assertEqual(self.action.error, "Invalid username or password - can not validate")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
