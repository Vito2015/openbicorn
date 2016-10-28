#!/usr/bin/env python
# coding: utf-8

# gunkeeperthrift - zooServer listened endpoints
bind = ['0.0.0.0:9090', '0.0.0.0:9091', '0.0.0.0:9093']


# gunicorn worker process count
# default, the value of the WEB_CONCURRENCY environment variable
# If it is not defined, the default is cpu core count
# workers = 1


# used for `thrift.config.WorkerClass`
# if PY < 2.8 : thrift_sync; else thriftpy_sync
# thrift_gevent | thrift_sync | thriftpy_sync
worker_class = 'thrift_sync'


#
# set thrift transport
# DEFAULT
# if PY < 2.8 :
#   'thrift.transport.TTransport:TBufferedTransportFactory'
# else :
#   'thriftpy.transport:TBufferedTransportFactory'
#
thrift_transport_factory = 'thrift.transport.TTransport:TBufferedTransportFactory'


#
# set thrift protocol
# DEFAULT
# if PY < 2.8 :
#   'thrift.protocol.TBinaryProtocol:TBinaryProtocolAcceleratedFactory'
# else :
#   'thriftpy.protocol:TBinaryProtocolFactory'
#
thrift_protocol_factory = 'thrift.protocol.TBinaryProtocol:TBinaryProtocolAcceleratedFactory'


# set service_register_cls for `gunicorn_thrift.config.ServiceRegisterClass`
service_register_cls = 'thriftzoo.register:ZookeeperRegister'


# set service_register_conf for `gunicorn_thrift.config.ServiceRegisterConf`
service_register_conf = {
    # addr field for register server endpoint
    'addr': '127.0.0.1:2181',

    # path field for register server uri path
    'path': '/test/gunicorn-zk-thrift/server'
}
