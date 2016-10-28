#!/usr/bin/env python
# coding: utf-8

__all__ = ['multiplexed_processor', ]


def multiplexed_processor(*args):
    try:
        import thrift
    except ImportError:
        raise RuntimeError("You need thrift installed to use 'multiplexed_processor'.")
    from thrift.TMultiplexedProcessor import TMultiplexedProcessor
    app = TMultiplexedProcessor()
    for servName, serv in args:
        app.registerProcessor(servName, serv)
    return app
