#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append('./gen-py')
sys.path.append('../env/lib')

from bicorn import multiplexed_processor

import serv_helloworld
import serv_helloworld2
import serv_geolocate


app = multiplexed_processor(
    ("HelloWorldService", serv_helloworld.service),
    ("HelloWorldService2", serv_helloworld2.service),
    ("GeolocateService", serv_geolocate.service)
)
