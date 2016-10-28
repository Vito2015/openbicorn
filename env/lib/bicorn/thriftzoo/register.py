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
        self.settings = {}

    def setup(self):
        pass

    def __getattr__(self, name):
        if name not in self.settings:
            raise AttributeError("No configuration setting for: %s" % name)
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


class ZookeeperRegister(Register):

    def __init__(self, conf, app):
        self.zk = None
        self.log = None
        super(ZookeeperRegister, self).__init__(conf, app)
        self.parse_conf()
        self.setup()

    def setup(self):
        zk = KazooClient(hosts=self.addr)
        zk.start()
        self.zk = zk
        cfg = self.app.cfg
        log = cfg.logger_class(cfg)
        self.log = log

    @staticmethod
    def get_node_path(reg_path, host, port):
        address = host + ':' + str(port)
        node_path = '/'.join([reg_path, address])
        return node_path

    def get_node_data(self):
        """
        :return: your node data
        """
        node_data = self.path
        return node_data

    def register_instances(self, instances):
        if not instances:
            return
        ip = get_ipv4('eth0')
        for instance in instances:
            port = instance['port']['main']
            try:
                node_path = self.get_node_path(self.path, ip, port)
                node_data = self.get_node_data()
                self.zk.create(node_path, node_data, ephemeral=True)
                self.log.info('Success register instance %s' % node_path)
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
                self.log.info('Success remove instance %s' % node_path )
            except NoNodeError as e:
                self.log.error('No Node Error in remove: ' + str(e))
            except Exception as e:
                self.log.error('UnExcept Error: type=' + str(e.__class__) + ' messages=' + str(e))
