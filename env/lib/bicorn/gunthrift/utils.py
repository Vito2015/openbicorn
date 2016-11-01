#!/usr/bin/env python
# coding: utf-8

import os
import importlib
from gunicorn.errors import AppImportError
from .six import AVAILABLE_PROCESSER_TYPES


def multiplexed_processor(worker_class_str, services):
    # try:
    #     import thrift
    #     from thrift.TMultiplexedProcessor import TMultiplexedProcessor
    # except ImportError:
    #     try:
    #         import thriftpy
    #         from thriftpy.thrift import TMultiplexedProcessor
    #     except ImportError:
    #         raise RuntimeError("You need thrift installed to use 'multiplexed_processor'.")

    def try_register_processor(app_obj, sname, serv):
        processor_obj = load_obj(serv) if isinstance(serv, str) else serv
        if hasattr(app_obj, 'registerProcessor'):
            app_obj.registerProcessor(sname, processor_obj)
        elif hasattr(app_obj, 'register_processor'):
            app_obj.register_processor(sname, processor_obj)
        else:
            raise TypeError("Wrong TMultiplexedProcessor type, %s", app_obj)

    def get_services(app_obj):
        for field_name in ['services', 'processors']:
            if hasattr(app_obj, field_name):
                return getattr(app_obj, field_name)

    processor_type = AVAILABLE_PROCESSER_TYPES.get(worker_class_str)
    if processor_type:
        app = load_obj(processor_type)()
    else:
        raise RuntimeError("Invalid %s for 'TMultiplexedProcessor'." % worker_class_str)
    # app = TMultiplexedProcessor()

    if isinstance(services, dict):
        services = services.items()
    elif isinstance(services, list):
        pass

    for servName, serv in services:
        try_register_processor(app, servName, serv)
        # app.register_processor(servName, load_obj(serv))
    # try:
    #     for servName, serv in services:
    #         # try_register_processor(app, servName, load_obj(serv))
    #         raise ValueError(app)
    #         app.register_processor(servName, load_obj(serv))
    # except TypeError as e:
    #     raise e
    # except:
    #     raise AppImportError(
    #         "Wrong multiplexed processors, {processorName:processor} please")
    return app, get_services(app)


def load_obj(import_path):
    parts = import_path.split(":", 1)
    if len(parts) == 1:
        raise ValueError("Wrong import path, module:obj please")

    module, obj = parts[0], parts[1]

    try:
        mod = importlib.import_module(module)
    except ImportError:
        if module.endswith(".py") and os.path.exists(module):
            raise ImportError(
                "Failed to find application, did "
                "you mean '%s:%s'?" % (module.rsplit(".", 1)[0], obj)
                )
        else:
            raise

    try:
        app = getattr(mod, obj)
    except AttributeError:
        raise AppImportError("Failed to find application object: %r" % obj)

    return app


class ProcessorMixin(object):
    def get_thrift_processor(self):
        return self.app.thrift_app.get_processor() if \
            self.app.cfg.thrift_processor_as_factory else \
            self.app.thrift_app

    def handle_processor_receive(self, listener, client, addr):
        sock_name = client.getsockname()
        # self.log.info('client %s', dir(client))
        self.log.info('Received messages: %s -> %s', "%s:%s" % (addr[0], addr[1]),
                      "%s:%s" % (sock_name[0], sock_name[1]))
