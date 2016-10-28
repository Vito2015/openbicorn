#!/usr/bin/env python
# coding: utf-8

import sys
import multiprocessing
PY_VERSION = sys.version_info[:3]

DEFAULT_WORKER_COUNT = multiprocessing.cpu_count()

if PY_VERSION <= (2, 8, 0):
    DEFAULT_WORKER = "thrift_sync"
    DEFAULT_TRANSPORT = "thrift.transport.TTransport:TBufferedTransportFactory"
    DEFAULT_PROTOCOL = \
        "thrift.protocol.TBinaryProtocol:TBinaryProtocolAcceleratedFactory"
    AVAILABLE_WORKERS = {
        'thrift_sync': 'gunthrift.sync_worker.SyncThriftWorker',
        'thrift_gevent': 'gunthrift.gevent_worker.GeventThriftWorker',
        'thriftpy_sync': 'gunthrift.thriftpy_sync_worker.SyncThriftPyWorker',
        'thriftpy_gevent': 'gunthrift.thriftpy_gevent_worker.GeventThriftPyWorker',
        }
else:
    DEFAULT_WORKER = "thriftpy_sync"
    DEFAULT_TRANSPORT = "thriftpy.transport:TBufferedTransportFactory"
    DEFAULT_PROTOCOL = "thriftpy.protocol:TBinaryProtocolFactory"
    AVAILABLE_WORKERS = {
        'thriftpy_sync': 'gunthrift.thriftpy_sync_worker.SyncThriftPyWorker',
        'thriftpy_gevent': 'gunthrift.thriftpy_gevent_worker.GeventThriftPyWorker',
        }
