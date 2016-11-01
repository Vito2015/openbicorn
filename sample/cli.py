#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append('./gen-py')

from HelloWorldService import HelloWorld

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TCompactProtocol
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol

# from thriftpy.protocol import binary
# from thriftpy.protocol.multiplex import TMultiplexedProtocol

try:
    host = '10.232.46.28'
    port = 9091
    transport = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(transport)

    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # protocol = binary.TBinaryProtocol(transport)
    protocol1 = TMultiplexedProtocol(protocol, 'HelloWorldService')
    client1 = HelloWorld.Client(protocol1)

    transport.open()

    print "client - ping"
    print "server - " + client1.ping()

    print "client - say"
    msg = client1.say("Hello!")
    print "server - " + msg

    transport.close()

except Thrift.TException, ex:
    print "%s" % (ex.message)