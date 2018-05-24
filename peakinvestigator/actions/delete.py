## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

from datetime import datetime

from .base import BaseAction

class DeleteAction(BaseAction):
    """This class is used to make a DELETE call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#DELETE.
    
    """
    
    def __init__(self, version, username, password, job):
        """Constructor."""
        
        super(DeleteAction,self).__init__(version, username, password)
        self._job = job

    def build_query(self):
        query = super(DeleteAction,self).build_query()
        query["Action"] = "DELETE"
        query["Job"] = self._job
        return query
    
    @property
    def last_changed(self):
        """Date and time when job was deleted. Returns a datetime object."""
        
        super(DeleteAction,self).precheck()
        return datetime.strptime(self._data["Datetime"], "%Y-%m-%d %H:%M:%S")
    
    @property
    def job(self):
        """Job identifier."""
        
        super(DeleteAction,self).precheck()
        return self._data["Job"]
    
