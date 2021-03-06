#!/usr/bin/env python
# coding: utf-8

import errno
import socket
import logging

try:
    import thrift
except ImportError:
    raise RuntimeError("You need thrift installed to use this worker.")

from thrift.transport import TSocket
from thrift.transport import TTransport

from gunicorn.workers.sync import SyncWorker

from .utils import ProcessorMixin

logger = logging.getLogger(__name__)


class SyncThriftWorker(SyncWorker, ProcessorMixin):
    def get_thrift_transports_and_protos(self, result):
        itrans = self.app.transport_factory.getTransport(result)
        otrans = self.app.transport_factory.getTransport(result)
        iprot = self.app.protocol_factory.getProtocol(itrans)
        oprot = self.app.protocol_factory.getProtocol(otrans)

        return (itrans, otrans), (iprot, oprot)

    def handle(self, listener, client, addr):
        self.cfg.on_connected(self, addr)
        if self.app.cfg.thrift_client_timeout is not None:
            client.settimeout(self.app.cfg.thrift_client_timeout)

        result = TSocket.TSocket()
        result.setHandle(client)

        try:
            (itrans, otrans), (iprot, oprot) = \
                self.get_thrift_transports_and_protos(result)

            processor = self.get_thrift_processor()

            try:
                while True:
                    self.handle_processor_receive(listener, client, addr)
                    processor.process(iprot, oprot)
                    self.notify()
            except TTransport.TTransportException:
                pass
            except thrift.Thrift.TException as e:
                self.log.error(e.message)
        except socket.error as e:
            if e.args[0] == errno.ECONNRESET:
                self.log.debug(e)
            else:
                self.log.exception(e)
        except Exception as e:
            self.log.exception(e)
        finally:
            itrans.close()
            otrans.close()
            self.cfg.post_connect_closed(self)

    def handle_quit(self, sig, frame):
        ret = super(SyncThriftWorker, self).handle_exit(sig, frame)
        self.cfg.worker_term(self)
        return ret
