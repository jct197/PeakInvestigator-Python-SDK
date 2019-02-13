## -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Veritomyx, Inc.
#
# This file is part of the Python SDK for PeakInvestigator
# (http://veritomyx.com) and is distributed under the terms
# of the BSD 3-Clause license.
import zlib
import struct
import six

def save_binary(headers,data_points,handle):
    for item in headers:
        handle.write(six.b("# %s" % item))
    handle.write(six.b('$'))
    compress = zlib.compressobj()
    handle.write(compress.compress(struct.pack('>q', len(data_points))))
    for i, j in data_points:
        mass = struct.pack('>d', i)
        height = struct.pack('>d', j)
        compressed_data = compress.compress(mass)
        handle.write(compressed_data)
        compressed_data = compress.compress(height)
        handle.write(compressed_data)
    compressed_data = compress.flush()
    handle.write(compressed_data)
    handle.write(six.b('\n'))