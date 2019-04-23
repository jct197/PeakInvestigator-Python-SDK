# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.

import unittest

from context import peakinvestigator

from peakinvestigator.io import save_binary

import tempfile
import six


class TestBinary(unittest.TestCase):

    def setUp(self):
        self.testempty = '$x\x9cc`\x80\x00\x00\x00\x08\x00\x01\n'
        self.testheader = '# This is a header\n# it should ' \
                          'contain meta data\n# There is no limit to ' \
                          'number of lines, and is optional.' \
                          '\n$x\x9cc`\x80\x00\x00\x00\x08\x00\x01\n'
        self.testfull = '# This is a header\n# it should contain meta data' \
                        '\n# There is no limit to number of lines, ' \
                        'and is optional.\n$x\x9cc`\x00\x03f\x87' \
                        '\xc9^`\x86C\xc0\x8f\xaf\x87\xfac4\x81|' \
                        '\xdb\x82\xc5\xd7\xb9\x1c\x82w\xce\x04' \
                        '\x82Y@\xbe\xcb\xec\xa5\x8fC\x1c\xc2\x1c' \
                        '\xc0\xea\x00\xbb\xdc\x11\xba\n'

    def test_empty(self):
        headers = []
        data_points = []
        with tempfile.TemporaryFile() as temp:
            save_binary(headers, data_points, handle=temp)
            temp.seek(0)
            f1 = temp.read()
        with tempfile.TemporaryFile() as temp2:
            temp2.write(six.b(self.testempty))
            temp2.seek(0)
            f2 = temp2.read()
        self.assertEqual(f1, f2)

    def test_header(self):
        headers = ['This is a header\n', 'it should contain meta data\n',
                   'There is no limit to number of lines, and is optional.\n']
        data_points = []
        with tempfile.TemporaryFile() as temp:
            save_binary(headers, data_points, handle=temp)
            temp.seek(0)
            f1 = temp.read()
        with tempfile.TemporaryFile() as temp2:
            temp2.write(six.b(self.testheader))
            temp2.seek(0)
            f2 = temp2.read()
        self.assertEqual(f1, f2)

    def test_full(self):
        headers = ['This is a header\n', 'it should contain meta data\n',
                   'There is no limit to number of lines, and is optional.\n']
        data_points = [[1234.5, 67.89], [1234.56, 78.9], [1234.567, 89.0]]
        with tempfile.TemporaryFile() as temp:
            save_binary(headers, data_points, handle=temp)
            temp.seek(0)
            f1 = temp.read()
        with tempfile.TemporaryFile() as temp2:
            temp2.write(six.b(self.testfull))
            temp2.seek(0)
            f2 = temp2.read()
        self.assertEqual(f1, f2)


if __name__ == "__main__":
    unittest.main()
