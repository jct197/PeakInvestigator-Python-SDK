## -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.
from .base import BaseAction

class SandboxAction(BaseAction):
    """This class is used to make a call to the PeakInvestigator
    API via sandbox. See https://peakinvestigator.veritomyx.com/api/#SandBox.
    
    """

    def __init__(self, action, sandboxoption=None):
        """Constructor"""
        self.action = action
        self.sandboxoption = sandboxoption

    def build_query(self):
        """Build query through sandbox."""
        query = self.action.build_query()
        if self.sandboxoption != None:
            query['Sandbox'] = self.sandboxoption
        else:
            query['Sandbox'] = '0'
        return query

    def process_response(self,response):
        """Process response through sandbox."""
        return self.action.process_response(response)

    def __getattr__(self, name):
        return getattr(self.action, name)