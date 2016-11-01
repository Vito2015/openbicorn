#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append('./gen-py')
sys.path.append('../env/lib')

from bicorn import multiplexed_processor

from conf import worker_class

import serv_helloworld


app, _ = multiplexed_processor(
    worker_class,
    [
        ("HelloWorldService", serv_helloworld.service)
    ],
)
