## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.


from abc import ABCMeta, abstractmethod
from six import with_metaclass
import decimal

import simplejson

@add_metaclass(Meta)
class BaseAction():
    """Abstract base class for a PeakInvestigator API action.
    """


    def __init__(self, version, username, password):
        """Constructor
        """
        
        self.version = version
        self.username = username
        self.password = password
        
    
    @abstractmethod
    def build_query(self):
        """Builds the query for the API call.
        
        Returns a dictionary containing all the info necessary.
        """
        
        return dict(Version=self.version, User=self.username, Code=self.password)
    
    
    def process_response(self, response):
        """Process the response (a string) of an API call. If the response 
        appears to be HTML, an exception is raised.

        """
        
        if '<' in response:
            raise Exception("Given response appears to be HTML, not JSON.")

        self._data = simplejson.loads(response, parse_float=decimal.Decimal)


    def precheck(self):
        """Make sure that the _data attribute has been set (i.e. after call to execute()).
        Throws an exception if it has not been set.
        """

        if not hasattr(self, "_data"):
            raise Exception("API response is missing. Has execute() been called ?")
        
    
    @property
    def error(self):
        """Returns the error message, or raises an exception if there wasn't 
        an error.
        
        """
        
        self.precheck()
        if "Error" not in self._data:
            return None

        return self._data["Message"]
