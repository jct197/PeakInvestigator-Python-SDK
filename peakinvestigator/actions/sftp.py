## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

from .base import BaseAction

class SftpAction(BaseAction):
    """This class is used to make a SFTP call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#SFTP.
    
    """


    def __init__(self, version, username, password, project_id):
        """Constructor
        
        """
        
        super(SftpAction,self).__init__(version, username, password)
        self.project_id = project_id
        
    
    def build_query(self):
        query = super(SftpAction,self).build_query()
        query["Action"] = "SFTP"
        query["ID"] = self.project_id
        return query
    
    
    @property
    def host(self):
        """Host to use for SFTP transfers."""
        
        super(SftpAction,self).precheck()
        return self._data["Host"]
    
    
    @property
    def port(self):
        """Port to use for SFTP transfers."""
        
        super(SftpAction,self).precheck()
        return self._data["Port"]
    
    
    @property
    def directory(self):
        """Directory on SFTP server to place files."""
        
        super(SftpAction,self).precheck()
        return self._data["Directory"]
    
    
    @property
    def sftp_username(self):
        """Username for SFTP transfers."""
        
        super(SftpAction,self).precheck()
        return self._data["Login"]
    
    
    @property
    def sftp_password(self):
        """Password for SFTP transfers."""
        
        super(SftpAction,self).precheck()
        return self._data["Password"]
    
    
    @property
    def fingerprints(self):
        """List of dictionary objects representing SFTP fingerprints. Keys
        should include Signature (e.g. DSA), 'Algorithm' (e.g. MD5), and 
        'Hash'.
        
        """
        
        super(SftpAction,self).precheck()
        return self._data["Fingerprints"]
    
    
