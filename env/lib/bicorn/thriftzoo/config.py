#!/usr/bin/env python
# coding: utf-8

from gunicorn import six
from gunicorn.config import Setting, validate_string, validate_pos_int,\
    WorkerClass, validate_callable, validate_bool, validate_dict

from gunthrift.six import DEFAULT_WORKER, DEFAULT_TRANSPORT, DEFAULT_PROTOCOL


#
# custom config
#
