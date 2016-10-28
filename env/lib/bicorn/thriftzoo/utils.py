#!/usr/bin/env python
# coding: utf-8

import socket
import struct
import fcntl


def get_ipv4(ethname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0X8915,
        struct.pack('256s', ethname[:15])
        )[20:24])
    return ip
