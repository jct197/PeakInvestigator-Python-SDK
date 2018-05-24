## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

from .base import BaseAction

class RunAction(BaseAction):
    """This class is used to make a RUN call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#RUN.
    
    It is constructed with a Fluent API because of the number of required
    arguments.
    
    """


    def __init__(self, version, username, password, jobID,
                    response_time_objective):
        """Constructor
        
        """
        
        super(RunAction,self).__init__(version, username, password)
        self._jobID = jobID
        self._response_time_objective = response_time_objective
        
        
    def with_files(self, *args, **kwds):
        """Specify the production and calibration data files using either
        function arguments or keywords.
        
        First try keywords. If those are missing, use args[0] for production and
        args[1] for calibration, if it exists.
        
        """
        
        if "production" in kwds:
            self._production = kwds["production"]
        else:
            self._production = args[0]
            
        if "calibration" in kwds:
            self._calibration = kwds["calibration"]
        elif len(args) == 2:
            self._calibration = args[1]
        
        return self
    
    
    def build_query(self):
        query = super(RunAction,self).build_query()
        
        query["Action"] = "RUN"
        query["Job"] = self._jobID
        query["RTO"] = self._response_time_objective
        query["InputFile"] = self._production
        if hasattr(self, "_calibration"):
            query["CalibrationFile"] = self._calibration
        
        return query


    @property
    def job(self):
        super(RunAction,self).precheck()
        return self._data["Job"]
    
