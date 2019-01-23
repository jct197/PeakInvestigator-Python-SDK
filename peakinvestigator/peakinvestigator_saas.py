## -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

import os
import requests
import tarfile
import zipfile
import glob
from paramiko.client import SSHClient, WarningPolicy
from peakinvestigator.progress.uploader import Uploader


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

    def __init__(self, *args, **kwds):
        """Constructor. If the 'server' keyword is specified, that is used for 
        the API calls. Otherwise, it will try to use the first argument. Note 
        that only the hostname without any path should be specified. If neither
        keywords or arguments are specified, it will default to
        https://peakinvestigator.veritomyx.com.
        
        https:// will be pre-pended if it is missing.
                     
        """
        
        if "server" in kwds:
            server = kwds["server"]
        elif len(args) > 0:
            server = args[0]
        else:
            server = "https://peakinvestigator.veritomyx.com"
            
        if "http" not in server:
            server = "https://" + server
            
        self._server = server
        
    def execute(self, action):
        """Call the API with the given action. An action should implement a
        build_query() method that returns a dictionary containing the 
        appropriate parameters for the HTTP POST request.
        
        This method returns the response from the server as a string, which
        is usually processed with the same action.
        
        """
        
        response = requests.post(self._server + "/api/", data=action.build_query())
        return response.text
        
    def upload(self, upload_action, local_file, progress_factory, num_scan=0):
        """Upload file to a SFTP server"""
        upload_action.num = num_scan
        uploader = Uploader(upload_action.host, upload_action.token, progress_factory)
        if os.path.exists(local_file):
            if tarfile.is_tarfile(local_file):
                uploader.upload_tarfile(local_file)
            elif zipfile.is_zipfile(local_file):
                uploader.upload_zipfile(local_file)
            else:
                uploader.upload_file(local_file, int(upload_action.num))
        else:
            filenames = glob.glob(local_file)
            uploader.upload_files(filenames)

        uploader.close()

    def download(self, sftp_action, remote_file, local_file, callback=None):
        """Download a file from a SFTP server."""
        
        with SSHClient() as ssh:
            ssh.set_missing_host_key_policy(WarningPolicy())
            ssh.connect(sftp_action.host, port=sftp_action.port,
                            username=sftp_action.sftp_username,
                            password=sftp_action.sftp_password)
            with ssh.open_sftp() as sftp:
                sftp.get(remote_file, local_file, callback)