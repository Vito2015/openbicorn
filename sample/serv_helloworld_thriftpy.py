#!/usr/bin/env python
# coding: utf-8
import os
import sys
import thriftpy
from thriftpy.thrift import TProcessor

helloworld_thrift = thriftpy.load("helloworld.thrift", module_name="helloworld_thrift")


class HelloWorldHandler:
  def ping(self):
    return "pong"

  def say(self, msg):
    ret = "Received [%s]:  %s" % (os.getpid(), msg)
    print(ret)
    sys.stdout.flush()
    return ret

service = TProcessor(helloworld_thrift.HelloWorld, HelloWorldHandler())
