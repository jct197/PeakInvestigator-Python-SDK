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

class TestRunAction(unittest.TestCase):
    
    def setUp(self):
        self.action = RunAction("4.2", "joe", "badpw", "J-1234", "RTO-24")
        
    def test_build_query1(self):
        """Test full case"""
        
        self.action.with_files("production.data.tar", "calibration.data.tar")
        query = self.action.build_query()
        
        self.assertEqual("RUN", query["Action"])
        self.assertEqual("4.2", query["Version"])
        self.assertEqual("joe", query["User"])
        self.assertEqual("badpw", query["Code"])
        self.assertEqual("J-1234", query["Job"])
        self.assertEqual("RTO-24", query["RTO"])
        self.assertEqual("production.data.tar", query["InputFile"])
        self.assertEqual("calibration.data.tar", query["CalibrationFile"])
        
    def test_build_query2(self):
        """Test without calibration"""
        
        self.action.with_files("production.data.tar")
        query = self.action.build_query()
        
        self.assertEqual("production.data.tar", query["InputFile"])
        self.assertNotIn("CalibrationFile", query)
        
    def test_build_query3(self):
        """ Test using keywords without calibration"""
        
        self.action.with_files(production="production.data.tar")
        query = self.action.build_query()
        
        self.assertEqual("production.data.tar", query["InputFile"])
        self.assertNotIn("CalibrationFile", query)
        
    def test_build_query4(self):
        """ Test using keywords with calibration"""
        
        self.action.with_files(calibration="calibration.data.tar",
                                production="production.data.tar")
        query = self.action.build_query()
        
        self.assertEqual("production.data.tar", query["InputFile"])
        self.assertEqual("calibration.data.tar", query["CalibrationFile"])
        
    def test_response(self):
        response = '{"Action":"RUN", "Job":"P-504.1463"}'
        self.action.process_response(response)
        
        self.assertEqual("P-504.1463", self.action.job)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()