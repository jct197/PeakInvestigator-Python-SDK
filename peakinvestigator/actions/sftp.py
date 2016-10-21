from .base import BaseAction

class SftpAction(BaseAction):
    """This class is used to make a SFTP call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#SFTP.
    
    """


    def __init__(self, version, username, password, project_id):
        """Constructor
        
        """
        
        super().__init__(version, username, password)
        self.project_id = project_id
        
    
    def build_query(self):
        query = super().build_query()
        query["Action"] = "SFTP"
        query["ID"] = self.project_id
        return query
    
    
    @property
    def host(self):
        """Host to use for SFTP transfers."""
        
        super().precheck()
        return self._data["Host"]
    
    
    @property
    def port(self):
        """Port to use for SFTP transfers."""
        
        super().precheck()
        return self._data["Port"]
    
    
    @property
    def directory(self):
        """Directory on SFTP server to place files."""
        
        super().precheck()
        return self._data["Directory"]
    
    
    @property
    def sftp_username(self):
        """Username for SFTP transfers."""
        
        super().precheck()
        return self._data["Login"]
    
    
    @property
    def sftp_password(self):
        """Password for SFTP transfers."""
        
        super().precheck()
        return self._data["Password"]
    
    
    @property
    def fingerprints(self):
        """List of dictionary objects representing SFTP fingerprints. Keys
        should include Signature (e.g. DSA), 'Algorithm' (e.g. MD5), and 
        'Hash'.
        
        """
        
        super().precheck()
        return self._data["Fingerprints"]
    
    