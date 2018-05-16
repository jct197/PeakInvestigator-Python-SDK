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

class TestInitAction(unittest.TestCase):
    
    def setUp(self):
        self.action = InitAction("4.2", "joe", "badpw", 1234, "1.3")
        

    def test_build_query1(self):
        """Specifies clientKey and mass range and metadata with arguments."""

        self.action.with_scan_count(123, 0).with_meta_data(100, 2000, 12345)
        self.action.with_mass_range(200, 1800).with_client_key("PythonTest")
        query = self.action.build_query()
        
        self.assertEqual("4.2", query["Version"])
        self.assertEqual("joe", query["User"])
        self.assertEqual("badpw", query["Code"])
        self.assertEqual("INIT", query["Action"])
        self.assertEqual(1234, query["ID"])
        self.assertEqual("1.3", query["PI_Version"])
        self.assertEqual(123, query["ScanCount"])
        self.assertEqual(0, query["CalibrationCount"])
        self.assertEqual(12345, query["MaxPoints"])
        self.assertEqual(100, query["MinMass"])
        self.assertEqual(2000, query["MaxMass"])
        self.assertEqual(200, query["StartMass"])
        self.assertEqual(1800, query["EndMass"])
        self.assertEqual("PythonTest", query["ClientKey"])


    def test_build_query2(self):
        """Mass range isn't specified."""

        self.action.with_scan_count(123, 0).with_meta_data(100, 2000, 12345)
        query = self.action.build_query()
        
        self.assertEqual("4.2", query["Version"])
        self.assertEqual("joe", query["User"])
        self.assertEqual("badpw", query["Code"])
        self.assertEqual("INIT", query["Action"])
        self.assertEqual(1234, query["ID"])
        self.assertEqual("1.3", query["PI_Version"])
        self.assertEqual(123, query["ScanCount"])
        self.assertEqual(0, query["CalibrationCount"])
        self.assertEqual(12345, query["MaxPoints"])
        self.assertEqual(100, query["MinMass"])
        self.assertEqual(2000, query["MaxMass"])
        self.assertEqual(100, query["StartMass"])
        self.assertEqual(2000, query["EndMass"])
        

    def test_build_query3(self):
        """Specifies mass range with keywords."""

        self.action.with_scan_count(123, 0).with_meta_data(100, 2000, 12345)
        self.action.with_mass_range(end=1800, start=200)
        query = self.action.build_query()
        
        self.assertEqual(200, query["StartMass"])
        self.assertEqual(1800, query["EndMass"])
        
        
    def test_response(self):
        response = '{"Action":"INIT", "Job":"V-504.1551", "ID":504, "Funds":115.01, ' + \
                        '"EstimatedCost":[{"Instrument":"TOF", "RTO":"RTO-24", "Cost":27.60}, ' + \
                        '{"Instrument":"Orbitrap", "RTO":"RTO-24", "Cost":36.22}, ' + \
                        '{"Instrument":"IonTrap", "RTO":"RTO-24", "Cost":32.59}]}'
        self.action.process_response(response)
        
        self.assertEqual("V-504.1551", self.action.job)
        self.assertEqual(Decimal("115.01"), self.action.funds)
        
        self.assertIn("TOF", self.action.instruments)
        self.assertIn("IonTrap", self.action.instruments)
        self.assertIn("Orbitrap", self.action.instruments)
        
        self.assertIn("RTO-24", self.action.response_time_objectives)
        
        self.assertEqual(Decimal("36.22"), self.action.cost("Orbitrap", "RTO-24"))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()