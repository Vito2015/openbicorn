#!/usr/bin/env python
# coding: utf-8

import os
from gunicorn import six
from gunicorn.config import Setting, validate_string, validate_pos_int, \
    WorkerClass, validate_callable, validate_bool, validate_dict

from .six import DEFAULT_WORKER, DEFAULT_TRANSPORT, DEFAULT_PROTOCOL, DEFAULT_WORKER_COUNT


WorkerClass.default = DEFAULT_WORKER


class ThriftTransportFactoryClass(Setting):
    name = "thrift_transport_factory"
    section = "Thrift"
    cli = ["--thrift-transport-factory"]
    validator = validate_string
    default = DEFAULT_TRANSPORT
    desc = """\
        The factory class for thrift transport.
    """


class ThriftProtocolFactoryClass(Setting):
    name = "thrift_protocol_factory"
    section = "Thrift"
    cli = ["--thrift-protocol-factory"]
    validator = validate_string
    default = DEFAULT_PROTOCOL
    desc = """\
        The factory class for thrift transport.
    """


class ThriftClientTimeout(Setting):
    name = "thrift_client_timeout"
    section = "Thrift"
    cli = ["--thrift-client-timeout"]
    validator = validate_pos_int
    default = None
    desc = """\
        Seconds to timeout a client if client is silent after this duration
    """


class ProcessorAsFactory(Setting):
    name = "thrift_processor_as_factory"
    section = "Thrift"
    cli = ["--thrift-processor-as-factory"]
    validator = validate_bool
    default = False
    desc = """\
        Treat app as processor factory instead of a single processor.
    """


class WorkerTerm(Setting):
    name = "worker_term"
    section = "Server Hooks"
    validator = validate_callable(1)
    type = six.callable

    def worker_term(worker):
        pass

    default = staticmethod(worker_term)
    desc = """\
        Called just after a worker received SIGTERM, and about to gracefully
        shutdown.

        The callable needs to accept one instance variable for the initialized
        Worker.
        """


class ClientConnected(Setting):
    name = "on_connected"
    section = "Server Hooks"
    validator = validate_callable(2)
    type = six.callable

    def on_connected(worker, addr):
        pass

    default = staticmethod(on_connected)
    desc = """\
        Called just after a connection is made.

        The callable needs to accept two instance variable for the worker and
        the connected client address.
        """


class ClientConnectClosed(Setting):
    name = "post_connect_closed"
    section = "Server Hooks"
    validator = validate_callable(1)
    type = six.callable

    def post_connect_closed(worker):
        pass

    default = staticmethod(post_connect_closed)
    desc = """\
        Called just after a connection is closed.

        The callable needs to accept one instance variable for the worker.
        """


class ServiceRegisterConf(Setting):
    name = "service_register_conf"
    section = "Service Register Conf"
    default = {}
    validator = validate_dict
    desc = """\
        Config used to connect to service register watcher
        """


class ServiceRegisterClass(Setting):
    name = "service_register_cls"
    section = "Service Register Class"
    cli = ["--service-register-cls"]
    validator = validate_string
    default = ''
    desc = """\
        The class used for register service
    """


class ThriftProcessorServices(Setting):
    name = "thrift_processor_services"
    section = "Thrift"
    default = {}
    validator = validate_dict
    desc = """\
        Called when server starting.

        for loading processor services
        """


class WhenReady(Setting):
    name = "when_ready"
    section = "Server Hooks"
    validator = validate_callable(1)
    type = six.callable

    def when_ready(server):
        pass
    default = staticmethod(when_ready)
    desc = """\
        Called just after the server is started.

        The callable needs to accept a single instance variable for the Arbiter.
        """


class Workers(Setting):
    name = "workers"
    section = "Worker Processes"
    cli = ["-w", "--workers"]
    meta = "INT"
    validator = validate_pos_int
    type = int
    default = int(os.environ.get('WEB_CONCURRENCY', DEFAULT_WORKER_COUNT))
    desc = """\
        The number of worker processes for handling requests.

        A positive integer generally in the 2-4 x $(NUM_CORES) range. You'll
        want to vary this a bit to find the best for your particular
        application's work load.

        By default, the value of the WEB_CONCURRENCY environment variable. If
        it is not defined, the default is 1.
        """
