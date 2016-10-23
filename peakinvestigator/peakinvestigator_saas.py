## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

import requests

class PeakInvestigatorSaaS(object):
    """"An object for interacting with the PeakInvestigator API. See 
    http://veritomyx.com for more information about PeakInvestigtor and 
    https://peakinvestigator.veritomyx.com/api for information about the
    public API.
    
    Here's an example::
    
        service = PeakInvestigatorSaaS("https://peakinvestigator.veritomyx.com")
        action = PiVersionsAction("4.2", "joe", "badpw")
        response = service.execute(action)
        action.process_response(response)
        
    See other documentation for more details.
    
    """

    def __init__(self, server):
        """Constructor.
          server - a string containing the address of the server
                     (e.g. https://peakinvestigator.veritomyx.com). It should
                     NOT include any path.
                     
        """
        
        self.server = server
        
    def execute(self, action):
        """Call the API with the given action. An action should implement a
        build_query() method that returns a dictionary containing the 
        appropriate parameters for the HTTP POST request.
        
        This method returns the response from the server as a string, which
        is usually processed with the same action.
        
        """
        
        response = requests.post(self.server + "/api/", data=action.build_query())
        return response.text
        
        