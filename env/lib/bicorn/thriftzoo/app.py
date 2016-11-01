#!/usr/bin/env python
# coding: utf-8

import sys
import functools
from gunthrift.app import ThriftApplication
from gunthrift import utils as g_t_utils

# `config` is unused in this module
# but must be imported to register config
# options with gunicorn
from . import config


def on_when_ready(hook_func, hook_func_2):
    @functools.wraps(hook_func)
    def _on_when_ready(server):
        r = hook_func(server)
        hook_func_2(server)
        return r
    return _on_when_ready


class ThriftZooApplication(ThriftApplication):

    def __init__(self, *args, **kwargs):
        self.service_watcher = None
        super(ThriftZooApplication, self).__init__(*args, **kwargs)

    def _override_hook(self, hook_name, last_hook_func):
        hook_name_func = self.cfg.__getattr__(hook_name)
        if hook_name_func:
            self.cfg.set(hook_name, on_when_ready(hook_name_func, last_hook_func))
            pass
        else:
            pass

    def load_config(self):
        super(ThriftZooApplication, self).load_config()
        self._override_hook('when_ready', self.regist)
        self._override_hook('on_exit', self.un_regist)

    def regist(self, *args, **kwargs):
        if self.cfg.service_register_cls:
            service_register_cls = g_t_utils.load_obj(
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

    def un_regist(self, *args, **kwargs):
        service_watcher = self.service_watcher
        if service_watcher:
            instances = []
            for i in self.cfg.address:
                port = i[1]
                instances.append({'port': {"main": port},
                                  'meta': None,
                                  'state': 'up'})
            service_watcher.remove_instance(instances)

    def run(self):
        # don't use  super(ThriftZooApplication, self).run()
        super(ThriftApplication, self).run()


def run():
    from thriftzoo.app import ThriftZooApplication as App
    App("%(prog)s [OPTIONS] [APP_MODULE]").run()

