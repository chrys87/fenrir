#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys
import __main__

if not os.path.dirname(os.path.realpath(__main__.__file__)) in sys.path:
    sys.path.append(os.path.dirname(os.path.realpath(__main__.__file__)))

import fenrir
from daemonize import Daemonize

pid = "/tmp/fenrir.pid"

def main():
    app = fenrir.fenrir()
    app.proceed()
    del app

if __name__ == "__main__":
    daemon = Daemonize(app="fenrir-daemon", pid=pid, action=main)
    daemon.start()

