## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.


from .base import BaseAction

class PiVersionsAction(BaseAction):
    """This class is used to make a PI_VERSIONS call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#PI_VERSIONS.
    
    """

    def __init__(self, version, username, password):
        """Constructor"""
        
        super(PiVersionsAction,self).__init__(version, username, password)


    def build_query(self):
        query = super(PiVersionsAction,self).build_query()
        query["Action"] = "PI_VERSIONS"
        return query
    
    
    @property
    def current_version(self):
        """Current or newest version (recommended).
        
        Returns a string.
        
        """
        
        super(PiVersionsAction,self).precheck()
        return self._data["Current"]


    @property
    def last_used(self):
        """Version of PeakInvestigator most recently passed to an INIT 
        call (if available).
        
        Returns a string.
        
        """
        
        super(PiVersionsAction,self).precheck()
        return self._data["LastUsed"]


    @property
    def count(self):
        """Number of PI versions available.
        
        Returns an integer.
        
        """
        
        super(PiVersionsAction,self).precheck()
        return int(self._data["Count"])


    @property
    def versions(self):
        """List of PeakInvestigator versions released including the Current 
        version, newest to oldest [<value>,<value>,...]
        
        """
        
        super(PiVersionsAction,self).precheck()
        return self._data["Versions"]
