#!/usr/bin/env python
# coding: utf-8


class ServerProxy(object):

    def __init__(self, conf, app):
        self.conf = conf
        self.app = app
        self.services = []

    def setup(self, *args, **kwargs):
        pass
