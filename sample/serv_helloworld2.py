#!/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.append('./gen-py')

from helloworld2 import HelloWorld2
from helloworld2.ttypes import *


class HelloWorldHandler2:
  def ping(self):
    return "pong2"

  def say(self, msg):
    ret = "Received2 [%s]:  %s" % (os.getpid(), msg)
    print ret
    sys.stdout.flush()
    return ret

service = HelloWorld2.Processor(HelloWorldHandler2())
