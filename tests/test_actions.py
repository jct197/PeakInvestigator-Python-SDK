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