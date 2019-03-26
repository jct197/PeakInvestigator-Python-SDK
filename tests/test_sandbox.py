## -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

import unittest, datetime
from decimal import Decimal

from context import peakinvestigator

from peakinvestigator.actions import *

class TestSandboxAction(unittest.TestCase):

    def test_responseInit(self):
        """Test Sandbox using Init Action"""
        actionInit = SandboxAction(InitAction("5.1", "user", "password", "100", "1.2")
                                        .with_mass_range(60, 80)
                                        .with_scan_count(5, 0)
                                        .with_meta_data(50, 100, 12345)
                                        .with_client_key('SDKTest'))
        response = """
        {
            "Action":"INIT",
            "Job":"V-504.1551",
            "ID":504, "Funds":115.01,
            "EstimatedCost":[{
                "Instrument":"TOF",
                "RTO":"RTO-24",
                "Cost":27.60
            },{
                "Instrument":"Orbitrap",
                "RTO":"RTO-24",
                "Cost":36.22
            },{
                "Instrument": "IonTrap",
                "RTO":"RTO-24",
                "Cost":32.59
            }]
        }
        """
        self.assertEqual(actionInit.build_query(),dict(Version="5.1", User="user",Code="password",Action="INIT",ID="100",PI_Version="1.2",
                                                            ScanCount=5,CalibrationCount=0,MaxPoints=12345,MinMass=50,MaxMass=100,StartMass=50,EndMass=100,ClientKey="SDKTest",Sandbox="0"))
        actionInit.process_response(response)
        self.assertEqual("V-504.1551",actionInit.job)
        self.assertEqual(504,actionInit.id)
        self.assertEqual(Decimal("115.01"),actionInit.funds)
        costs = actionInit.estimated_costs
        self.assertEqual(Decimal("27.60"),costs[0]['Cost'])
        self.assertEqual(Decimal("36.22"),costs[1]['Cost'])
        self.assertEqual(Decimal("32.59"),costs[2]['Cost'])

    def test_responseRun(self):
        """Test Sandbox using Run Action"""
        actionRun = SandboxAction(RunAction("5.1", "user", "password", "100", "RTO-24")
                                       .with_files("production.data.tar", "calibration.data.tar"))
        response = """
        {
            "Action": "RUN",
            "Job": "P-504.1463"
        }
        """
        self.assertEqual(actionRun.build_query(),dict(Version="5.1", User="user", Code="password", Action="RUN", Job="100", RTO="RTO-24",
                                                           InputFile="production.data.tar", CalibrationFile="calibration.data.tar", Sandbox="0"))
        actionRun.process_response(response)
        self.assertEqual("P-504.1463", actionRun.job)

    def test_responseStatus(self):
        """Test Sandbox using Status Action"""
        actionStatus = SandboxAction(StatusAction("5.1","user","password","100"))
        response1 = """
        {
            "Action":"STATUS",
            "Job":"P-504.5148",
            "Status":"Running",
            "Datetime":"2016-02-03 18:25:09"
        }
        """
        response2 = """
        {
            "Action":"STATUS",
            "Job":"P-504.5148",
            "Status":"Done",
            "Datetime":"2016-02-03 18:31:05",
            "ScansInput":3,
            "ScansComplete":3,
            "ActualCost":0.36,
            "ResultFiles":["Log","MassList"],
            "ResultFilePaths":{
                "Log":"/files/P-504.5148/P-504.5148.log.txt",
                "MassList":"/files/P-504.5148/P-504.5148.mass_list.tar"
            } 
        }
        """
        response3 = """
        {
            "Action":"STATUS",
            "Job":"P-504.1463",
            "Status":"Deleted",
            "Datetime":"2016-02-03 18:36:05"
        }
        """
        self.assertEqual(actionStatus.build_query(),dict(Version="5.1", User="user", Code="password", Action="STATUS",Job="100", Sandbox="0"))
        actionStatus.process_response(response1)
        self.assertEqual("P-504.5148",actionStatus.job)
        self.assertEqual("Running",actionStatus.status)
        self.assertEqual(False,actionStatus.done)
        self.assertEqual(datetime.datetime(2016, 2, 3, 18, 25, 9),actionStatus.last_changed)

        actionStatus.process_response(response2)
        self.assertEqual("P-504.5148",actionStatus.job)
        self.assertEqual("Done",actionStatus.status)
        self.assertEqual(True,actionStatus.done)
        self.assertEqual(datetime.datetime(2016, 2, 3, 18, 31, 5),actionStatus.last_changed)
        self.assertEqual(Decimal("0.36"),actionStatus.cost)
        self.assertEqual("/files/P-504.5148/P-504.5148.mass_list.tar",actionStatus.results_file)
        self.assertEqual("/files/P-504.5148/P-504.5148.log.txt",actionStatus.log_file)
        self.assertEqual(3,actionStatus.num_input_scans)
        self.assertEqual(3,actionStatus.num_completed_scans)

        actionStatus.process_response(response3)
        self.assertEqual("P-504.1463",actionStatus.job)
        self.assertEqual("Deleted",actionStatus.status)
        self.assertEqual(False,actionStatus.done)
        self.assertEqual(datetime.datetime(2016, 2, 3, 18, 36, 5),actionStatus.last_changed)

if __name__ == "__main__":
    unittest.main()
