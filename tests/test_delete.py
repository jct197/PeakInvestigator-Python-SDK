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

class TestDeleteAction(unittest.TestCase):
    
    def setUp(self):
        self.action = DeleteAction("4.2","joe", "badpw", "J-1234")
        
    def test_build_query(self):
        query = self.action.build_query()
        
        self.assertEqual("DELETE", query["Action"])
        self.assertEqual("4.2", query["Version"])
        self.assertEqual("joe", query["User"])
        self.assertEqual("badpw", query["Code"])
        self.assertEqual("J-1234", query["Job"])
        
    def test_response(self):
        response = '{"Action":"DELETE", "Job":"P-504.4256", "Datetime":"2016-02-03 18:35:06"}'
        self.action.process_response(response)
        
        self.assertEqual("P-504.4256", self.action.job)
        
        last_changed = self.action.last_changed
        
        self.assertEqual(2016, last_changed.year)
        self.assertEqual(2, last_changed.month)
        self.assertEqual(3, last_changed.day)
        self.assertEqual(18, last_changed.hour)
        self.assertEqual(35, last_changed.minute)
        self.assertEqual(6, last_changed.second)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()