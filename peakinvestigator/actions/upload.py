## -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.


from .base import BaseAction


class UploadAction(BaseAction):
    """This class is used to make an UPLOAD call to the PeakInvestigator
    API. See https://peakinvestigator.veritomyx.com/api/#UPLOAD.

    """

    def __init__(self, version, username, password, project_id, data_name):
        """Constructor"""

        super(UploadAction, self).__init__(version, username, password)
        self.project_id = project_id
        self.data_name = data_name

    def build_query(self):
        query = super(UploadAction, self).build_query()
        query["Action"] = "UPLOAD"
        query["ID"] = self.project_id
        return query

    @property
    def host(self):
        """Returns host.

        """

        super(UploadAction, self).precheck()
        return self._data["Host"]

    @property
    def port(self):
        """Returns port.

        """

        super(UploadAction, self).precheck()
        return self._data["Port"]

    @property
    def token(self):
        """Returns token for upload.

        """

        super(UploadAction, self).precheck()
        return self._data["Token"]

