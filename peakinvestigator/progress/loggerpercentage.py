# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.
from peakinvestigator.progress.progress import *
import logging
import time
import sys
import os

logging.getLogger('Progress')

class LogProgressPercent(Progress):

    def __init__(self, total, unit='scans'):
        self.total = total
        self.unit = unit
        self.count = 0
        self.clock = time.time()
        self.logger = logging.getLogger('Progress')
        self.logger.setLevel(logging.INFO)

    def update(self, update):
        self.count += update
        current = time.time()
        if round(self.count/self.total*100, 0) % 10 == 0:
            sys.stdout.write('\r'+str(round(self.count/self.total*100, 0))+str(' Percent'))
        if current - self.clock > 30:
            sys.stdout.write('\n')
            self.logger.info('Finished uploading {} of {} {}.'.format(self.count, self.total, self.unit))
            self.clock = current

    def close(self):
        sys.stdout.write('\n')
        self.logger.info('Finished upload of {} {}'.format(self.count, self.unit))

class LoggerProgressPercent(ProgressFactory):

    def __init__(self):
        pass

    def create(self, total, unit):
        return LogProgressPercent(total, unit)
