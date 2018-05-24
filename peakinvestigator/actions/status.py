## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.


from datetime import datetime

from .base import BaseAction

class StatusAction(BaseAction):
    """This class is used to make a STATUS call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#STATUS.
    
    """

    def __init__(self, version, username, password, job):
        """Constructor"""
        
        super(StatusAction,self).__init__(version, username, password)
        self._job = job
        
    def build_query(self):
        query = super(StatusAction,self).build_query()
        query["Action"] = "STATUS"
        query["Job"] = self._job
        return query
    
    @property
    def job(self):
        """Job identifier."""
        
        super(StatusAction,self).precheck()
        return self._data["Job"]
    
    @property
    def status(self):
        """Current state of job: 'Preparing', 'Running', 'Done', or 'Deleted'
        
          * Preparing – Input or calibration files being prepared (use PREP 
            call to get details)
          * Running – Job being processed
          * Done – Job complete, job information appended to results below 
          * Deleted – Job has been deleted from the server
        
        """
        
        super(StatusAction,self).precheck()
        return self._data["Status"]
    
    @property
    def done(self):
        """Convenience property indicating whether job is done. Returns a 
        boolean.
        
        """
        
        super(StatusAction,self).precheck()
        return self.status == "Done"
    
    @property
    def last_changed(self):
        """Date and time of last status change. Returns a datetime object."""
        
        super(StatusAction,self).precheck()
        return datetime.strptime(self._data["Datetime"], "%Y-%m-%d %H:%M:%S")
    
    @property
    def cost(self):
        """Actual cost (US$) of job charged to the Project. Returns a Decimal 
        object.
        
        """
        
        if not self.done:
            raise Exception("Job is not done.")

        return self._data["ActualCost"]
    
    @property
    def results_file(self):
        """Path of results file available in SFTP drop."""
        
        if not self.done:
            raise Exception("Job is not done.")
        
        return self._data["ResultsFile"]
    
    @property
    def log_file(self):
        """Path of job log file available in SFTP drop."""
        
        if not self.done:
            raise Exception("Job is not done.")
        
        return self._data["JobLogFile"]
    
    @property
    def num_input_scans(self):
        """Number of scans provided as input."""
        
        super(StatusAction,self).precheck()
        return self._data["ScansInput"]
    
    @property
    def num_completed_scans(self):
        """Number of scans completed and provided in results file."""
        
        super(StatusAction,self).precheck()
        return self._data["ScansComplete"]
    
    
    
