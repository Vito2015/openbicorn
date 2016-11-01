#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import sys
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import *

from .utils import get_ipv4

REGISTER_PARAM = ["auth", "addr", "path"]


class Register(object):
    """
    Base class of register
    """
    def __init__(self, conf, app):
        self.conf = conf
        self.app = app
        cfg = self.app.cfg
        self.log = cfg.logger_class(cfg)
        self.settings = {}
        self.parse_conf()
        self.setup()

    def setup(self):
        pass

    def __getattr__(self, name):
        if name not in self.settings:
            raise AttributeError("No configuration getting for: %s" % name)
        return self.settings[name]

    def set(self, name, value):
        if name not in REGISTER_PARAM:
            raise AttributeError("No configuration setting for: %s" % name)
        self.settings[name] = value

    def parse_conf(self):
        for k, v in self.conf.items():
            if k not in REGISTER_PARAM:
                continue
            try:
                self.set(k.lower(), v)
            except:
                print("Invalid value for %s: %s\n" % (k, v), file=sys.stderr)
                sys.stderr.flush()
                raise

    def register_instances(self, instances):
        pass

    def remove_instance(self, instances):
        pass

    def register_services(self, *services):
        pass

    def remove_services(self, *services):
        pass


class ZookeeperRegister(Register):

    def __init__(self, conf, app):
        self.zk = None
        self.log = None
        super(ZookeeperRegister, self).__init__(conf, app)

    def setup(self):
        zk = KazooClient(hosts=self.addr)
        zk.start()
        self.zk = zk

    @staticmethod
    def get_node_path(reg_path, host, port):
        address = host + ':' + str(port)
        node_path = '/'.join([reg_path, address])
        return node_path

    def get_services(self):
        """
        :return: services name strings (split by '|') which need regist
        """
        # node_data = self.path
        node_data = '|'.join(self.app.services_names)
        return node_data

    def register_instances(self, instances):
        if not instances:
            return
        ip = get_ipv4('eth0')
        self.log.info('serviceNames=%s', self.app.services_names)
        for instance in instances:
            port = instance['port']['main']
            try:
                node_path = self.get_node_path(self.path, ip, port)
                services = self.get_services()
                self.zk.create(node_path, services, ephemeral=True, makepath=True)
                self.log.info('Success registered instance %s {%s}' % (node_path, services))
            except NodeExistsError as e:
                self.log.error('ZNode Exists Error in Create: ' + str(e))
            except Exception as e:
                self.log.error('UnExcept Error: type=' + str(e.__class__) + ' messages=' + str(e))

    def remove_instance(self, instances):
        if not instances:
            return
        ip = get_ipv4('eth0')
        for instance in instances:
            port = instance['port']['main']
            try:
                node_path = self.get_node_path(self.path, ip, port)
                self.zk.delete(node_path, recursive=True)
                self.log.info('Success removed instance %s' % node_path)
            except NoNodeError as e:
                self.log.error('No Node Error in remove: ' + str(e))
            except Exception as e:
                self.log.error('UnExcept Error: type=' + str(e.__class__) + ' messages=' + str(e))

    def register_services(self, *services):
        if not services:
            return
        try:
            self.zk.set(self.path, '|'.join(services))
            self.log('Success registered: %s, services=%s' % (services, services))
        except Exception as e:
            self.log.error('UnExcept Error: type=' + str(e.__class__) + ' messages=' + str(e))

    def remove_services(self, *services):
        if not services:
            return
        try:
            register_services = (self.zk.get(self.path) or '').split('|')
            map(register_services.remove, services)
            self.zk.set(self.path, '|'.join(register_services))
            self.log('Success removed: %s, services=%s' % (services, register_services))
        except Exception as e:
            self.log.error('UnExcept Error: type=' + str(e.__class__) + ' messages=' + str(e))
