# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

from distutils.core import setup

setup(name="PeakInvestigator Python SDK", version="0.9",
        description="A library for interacting with the PeakInvestigator API",
        author="Adam Tenderholt",
        author_email="adam.tenderholt@veritomyx.com",
        url="http://veritomyx.com",
        packages=["peakinvestigator", "peakinvestigator.actions"])
