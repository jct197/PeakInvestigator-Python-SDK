## -*- coding: utf-8 -*-
# 
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

cd tests &&
python -m test_pi_versions &&
python -m test_init &&
python -m test_sftp &&
python -m test_run &&
python -m test_status &&
python -m test_delete 
