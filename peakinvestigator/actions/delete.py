from datetime import datetime

from .base import BaseAction

class DeleteAction(BaseAction):
    """This class is used to make a DELETE call to the PeakInvestigator 
    API. See https://peakinvestigator.veritomyx.com/api/#DELETE.
    
    """
    
    def __init__(self, version, username, password, job):
        """Constructor."""
        
        super().__init__(version, username, password)
        self._job = job

    def build_query(self):
        query = super().build_query()
        query["Action"] = "DELETE"
        query["Job"] = self._job
        return query
    
    @property
    def last_changed(self):
        """Date and time when job was deleted. Returns a datetime object."""
        
        super().precheck()
        return datetime.strptime(self._data["Datetime"], "%Y-%m-%d %H:%M:%S")
    
    @property
    def job(self):
        """Job identifier."""
        
        super().precheck()
        return self._data["Job"]
    