
from .base import BaseAction

class PiVersionsAction(BaseAction):
    """This class is used to make a PI_VERSIONS call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#PI_VERSIONS.
    
    """

    def __init__(self, version, username, password):
        """Constructor"""
        
        super().__init__(version, username, password)


    def build_query(self):
        query = super().build_query()
        query["Action"] = "PI_VERSIONS"
        return query
    
    
    @property
    def current_version(self):
        """Current or newest version (recommended).
        
        Returns a string.
        
        """
        
        super().precheck()
        return self._data["Current"]


    @property
    def last_used(self):
        """Version of PeakInvestigator most recently passed to an INIT 
        call (if available).
        
        Returns a string.
        
        """
        
        super().precheck()
        return self._data["LastUsed"]


    @property
    def count(self):
        """Number of PI versions available.
        
        Returns an integer.
        
        """
        
        super().precheck()
        return int(self._data["Count"])


    @property
    def versions(self):
        """List of PeakInvestigator versions released including the Current 
        version, newest to oldest [<value>,<value>,...]
        
        """
        
        super().precheck()
        return self._data["Versions"]
