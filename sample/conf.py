#!/usr/bin/env python
# coding: utf-8

# just for gunicorn worker process name, default "bicorn"
# default_proc_name = 'bicorn-test-service'

# bicorn.thriftzoo - zooServer listened endpoints
bind = ['0.0.0.0:9090', '0.0.0.0:9091', '0.0.0.0:9092']


# gunicorn worker process count
# default, the value of the WEB_CONCURRENCY environment variable
# If it is not defined, the default is cpu core count
# workers = 1


# used for `thrift.config.WorkerClass`
# if PY < 2.8 : thrift_sync; else thriftpy_sync
# thrift_gevent | thrift_sync | thriftpy_sync | thriftpy_gevent
#
# demo for thrift worker
# worker_class = 'thrift_sync'
#
# demo for thriftpy worker
worker_class = 'thriftpy_sync'


#
# set thrift transport
# DEFAULT
# if PY < 2.8 :
#   'thrift.transport.TTransport:TBufferedTransportFactory'
# else :
#   'thriftpy.transport:TBufferedTransportFactory'
#
# demo for thrift service
# thrift_transport_factory = 'thrift.transport.TTransport:TBufferedTransportFactory'
#
# demo for thriftpy service
thrift_transport_factory = 'thriftpy.transport:TBufferedTransportFactory'

#
# set thrift protocol
# DEFAULT
# if PY < 2.8 :
#   'thrift.protocol.TBinaryProtocol:TBinaryProtocolAcceleratedFactory'
# else :
#   'thriftpy.protocol:TBinaryProtocolFactory'
#
# demo for thrift service
# thrift_protocol_factory = 'thrift.protocol.TBinaryProtocol:TBinaryProtocolFactory'
#
# demo for thriftpy service
thrift_protocol_factory = 'thriftpy.protocol:TBinaryProtocolFactory'


# set service_register_cls for `bicorn.gunthrift.config.ServiceRegisterClass`
service_register_cls = 'thriftzoo.register:ZookeeperRegister'


# set service_register_conf for `bicorn.thriftzoo.config.ServiceRegisterConf`
service_register_conf = {
    # addr field for register server endpoint
    'addr': '127.0.0.1:2181',

    # path field for register server uri path
    'path': '/rpc/bicorn-services-miui-xiaomi-lg/miuisys/cdc/v1/testservice1'
}

# demo for thrift service
# thrift_processor_services = {
#     "HelloWorldService": 'serv_helloworld:service'
# }
#
# demo for thriftpy service
thrift_processor_services = {
    "HelloWorldService": 'serv_helloworld_thriftpy:service'
}
