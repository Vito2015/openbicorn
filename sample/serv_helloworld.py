#!/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.append('./gen-py')

from HelloWorldService import HelloWorld
from HelloWorldService.ttypes import *


class HelloWorldHandler:
  def ping(self):
    return "pong"

  def say(self, msg):
    ret = "Received [%s]:  %s" % (os.getpid(), msg)
    print(ret)
    sys.stdout.flush()
    return ret

service = HelloWorld.Processor(HelloWorldHandler())
