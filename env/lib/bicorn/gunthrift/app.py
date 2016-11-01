#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import os
import sys

from gunicorn.app.base import Application
from gunicorn.errors import AppImportError
import gunicorn.workers

# `config` is unused in this module but must be imported to register config
# options with gunicorn
from . import config
from . import utils
from .six import AVAILABLE_WORKERS

# register thrift workers

gunicorn.workers.SUPPORTED_WORKERS.update(AVAILABLE_WORKERS)


class ThriftApplication(Application):
    def __init__(self, *args, **kwargs):
        self.services = []
        self.services_names = []
        self.log = None
        self.app_uri = None
        self.transport_factory = None
        self.protocol_factory = None
        self.thrift_app = None
        self.service_watcher = None
        super(ThriftApplication, self).__init__(*args, **kwargs)
        self.services_names = self.cfg.thrift_processor_services.keys()
        self.log = self.cfg.logger_class(self.cfg)

    def init(self, parser, opts, args):
        if len(args) != 1:
            args.append("bicorn")
            self.cfg.logger_class(self.cfg).error("No application name specified.")
        self.cfg.set("default_proc_name", args[0])

        self.app_uri = args[0]

        if opts.worker_class and \
                opts.worker_class not in AVAILABLE_WORKERS:
            raise ValueError

    def load_thrift_app(self):
        if ':' in self.app_uri:
            app = utils.load_obj(self.app_uri)
        else:
            services = self.cfg.thrift_processor_services
            if isinstance(services, dict):
                app, self.services = utils.multiplexed_processor(self.cfg.worker_class_str, services)
            # elif isinstance(services, list):
            #     self.services_names = [x[0] for x in services if isinstance(x, (tuple, list))]
            #     app = utils.multiplexed_processor(*services)
            else:
                raise AppImportError("Invalid \"thrift_processor_services\" configuration. "
                                     "{processorName:processor} please")
        return app

    def load(self):
        self.chdir()
        self.transport_factory = utils.load_obj(self.cfg.thrift_transport_factory)()
        self.protocol_factory = utils.load_obj(self.cfg.thrift_protocol_factory)()
        self.thrift_app = self.load_thrift_app()
        return lambda: 1

    def chdir(self):
        os.chdir(self.cfg.chdir)
        sys.path.insert(0, self.cfg.chdir)

    def run(self):
        if self.cfg.service_register_cls:
            service_register_cls = utils.load_obj(
                self.cfg.service_register_cls)
            self.service_watcher = service_register_cls(
                self.cfg.service_register_conf, self)
            # generate the instances to register
            instances = []
            for i in self.cfg.address:
                port = i[1]
                instances.append({'port': {"main": port},
                                  'meta': None,
                                  'state': 'up'})
            self.service_watcher.register_instances(instances)
        super(ThriftApplication, self).run()


def run():
    from .app import ThriftApplication
    ThriftApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
