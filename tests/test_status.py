## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

import unittest
from decimal import Decimal

from context import peakinvestigator

from peakinvestigator.actions import *

class TestStatusAction(unittest.TestCase):
    
    def setUp(self):
        self.action = StatusAction("4.2", "joe", "badpw", "J-1234")
        
    def test_build_query(self):
        query = self.action.build_query()
        
        self.assertEqual("STATUS", query["Action"])
        self.assertEqual("4.2", query["Version"])
        self.assertEqual("joe", query["User"])
        self.assertEqual("badpw", query["Code"])
        self.assertEqual("J-1234", query["Job"])
        
    def test_response1(self):
        response = '{"Action":"STATUS", "Job":"P-504.5148", "Status":"Preparing", "Datetime":"2016-02-03 18:18:12"}'
        self.action.process_response(response)
    
        self.assertEqual("P-504.5148", self.action.job)
        self.assertEqual("Preparing", self.action.status)
        self.assertFalse(self.action.done)
        
        last_changed = self.action.last_changed
        
        self.assertEqual(2016, last_changed.year)
        self.assertEqual(2, last_changed.month)
        self.assertEqual(3, last_changed.day)
        self.assertEqual(18, last_changed.hour)
        self.assertEqual(18, last_changed.minute)
        self.assertEqual(12, last_changed.second)
        
    def test_response2(self):
        response = '{"Action":"STATUS", "Job":"P-504.5148", "Status":"Running", "Datetime":"2016-02-03 18:25:09"}'
        self.action.process_response(response)
        
        self.assertFalse(self.action.done)
        self.assertEqual("Running", self.action.status)
        
    def test_response3(self):
        response = '{"Action":"STATUS", "Job":"P-504.5148", "Status":"Done", "Datetime":"2016-02-03 18:31:05", ' + \
                    '"ScansInput":3, "ScansComplete":3, "ActualCost":0.36, ' + \
                    '"JobLogFile":"/files/P-504.5148/P-504.5148.log.txt", ' + \
                    '"ResultsFile":"/files/P-504.5148/P-504.5148.mass_list.tar"}'
        self.action.process_response(response)
        
        self.assertTrue(self.action.done)
        self.assertEqual("Done", self.action.status)
        self.assertEqual(3, self.action.num_input_scans)
        self.assertEqual(3, self.action.num_completed_scans)
        self.assertEqual(Decimal("0.36"), self.action.cost)
        self.assertEqual("/files/P-504.5148/P-504.5148.log.txt",
                            self.action.log_file)
        self.assertEqual("/files/P-504.5148/P-504.5148.mass_list.tar",
                            self.action.results_file)
        
    def test_response4(self):
        response = '{"Action":"STATUS", "Job":"P-504.1463", "Status":"Deleted", "Datetime":"2016-02-03 18:36:05"}'
        self.action.process_response(response)
        
        self.assertFalse(self.action.done)
        self.assertEqual("Deleted", self.action.status)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()