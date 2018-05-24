## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.


from .base import BaseAction

class InitAction(BaseAction):
    """This class is used to make an INIT call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#INIT
    
    It is constructed with a Fluent API because of the number of required
    arguments.
    
    """


    def __init__(self, api_version, username, password, project_id, pi_version):
        """Constructor
        
        """
        
        super(InitAction,self).__init__(api_version, username, password)
        self.project_id = project_id
        self.pi_version = pi_version
        
        
    def with_scan_count(self, production, calibration):
        """Set the number of production and calibration scans."""
        
        self.production = production
        self.calibration = calibration
        return self
        
    
    def with_meta_data(self, min_mass, max_mass, num_points):
        """Set the meta data required for processing data. This also sets the 
        desired starting and ending mass range to provided values by default, 
        which can be further specified with with_mass_range().
        
        """
        
        self.min_mass = min_mass
        self.max_mass = max_mass
        self.start_mass = min_mass
        self.end_mass = max_mass
        self.num_points = num_points
        return self
    
    
    def with_mass_range(self, *args, **kwds):
        """Set the desired mass range for processing.
        
        If arguments are provided, then the first is the starting range and the
        second is the ending range.
        
        If keywords are provided, start and end are used to specify the starting
        and ending range, respectively.

        """
        
        if len(args) == 2:
            self.start_mass = args[0]
            self.end_mass = args[1]
        elif "start" in kwds and "end" in kwds:
            self.start_mass = kwds["start"]
            self.end_mass = kwds["end"]
        else:
            raise Exception("Inappropriate arguments or keywords.")

        return self
    
    
    def with_client_key(self, client_key):
        """Set the (optional) client key."""
        
        self.client_key = client_key
        return self
    
    
    def build_query(self):
        query = super(InitAction,self).build_query()
        query["Action"] = "INIT"
        query["ID"] = self.project_id
        query["PI_Version"] = self.pi_version
        query["ScanCount"] = self.production
        query["CalibrationCount"] = self.calibration
        query["MaxPoints"] = self.num_points
        query["MinMass"] = self.min_mass
        query["MaxMass"] = self.max_mass
        query["StartMass"] = self.start_mass
        query["EndMass"] = self.end_mass
        if hasattr(self, "client_key"):
            query["ClientKey"] = self.client_key
        
        return query
    
    
    @property
    def job(self):
        """The job to be used in subsequent API calls (i.e. RUN, STATUS, and DELETE)."""
        
        super(InitAction,self).precheck()
        return self._data["Job"]
    
    
    @property
    def id(self):
        """The (sub)project used in the INIT call."""
        
        super(InitAction,self).precheck()
        return self._data["ID"]
    
    
    @property
    def funds(self):
        """The funds available to the project. Returns a Decimal object."""
        
        super(InitAction,self).precheck()
        return self._data["Funds"]

    
    @property
    def estimated_costs(self):
        """The estimated cost for the job. This returns a list of dictionaries 
        with "Instrument", "RTO", and "Cost" keys.
        
        """
        
        super(InitAction,self).precheck()
        return self._data["EstimatedCost"]
    
    
    @property
    def instruments(self):
        """The type of instruments available for processing. Returns a set."""
        super(InitAction,self).precheck()
        return set([ x["Instrument"] for x in self._data["EstimatedCost"] ])
    
    
    @property
    def response_time_objectives(self):
        """The RTOs available for processing. One RTO must be passed to the 
        INIT call. Returns a set.
        
        """
        
        super(InitAction,self).precheck()
        return set([ x["RTO"] for x in self._data["EstimatedCost"] ])
    
    
    def cost(self, instrument, response_time_objective):
        """Get the estimated job cost for a given instrument and RTO. Returns 
        a Decimal object.
        
        """
        
        super(InitAction,self).precheck()
        costs = [ x["Cost"] for x in self._data["EstimatedCost"] \
                    if x["Instrument"] == instrument and \
                        x["RTO"] == response_time_objective ]
        
        assert len(costs) == 1
        return costs[0]
    
