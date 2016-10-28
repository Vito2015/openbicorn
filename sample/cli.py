#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append('./gen-py')

from helloworld import HelloWorld
from helloworld2 import HelloWorld2

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TCompactProtocol
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol

try:
    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)

    # server default config of 'thrift_protocol_factory'
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    protocol1 = TMultiplexedProtocol(protocol, 'HelloWorldService')
    client1 = HelloWorld.Client(protocol1)

    protocol2 = TMultiplexedProtocol(protocol, 'HelloWorldService2')
    client2 = HelloWorld2.Client(protocol2)

    transport.open()

    print "client - ping"
    print "server - " + client1.ping()

    print "client - say"
    msg = client1.say("Hello!")
    print "server - " + msg

    print "client2 - ping"
    print "server2 - " + client2.ping()

    print "client2 - say"
    msg = client2.say("Hello!")
    print "server2 - " + msg

    transport.close()

except Thrift.TException, ex:
    print "%s" % (ex.message)