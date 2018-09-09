#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.remoteDriver import remoteDriver
from fenrirscreenreader.core.eventData import fenrirEventType

import select, socket, os, os.path


class driver(remoteDriver):
    def __init__(self):
        remoteDriver.__init__(self)
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['processManager'].addCustomEventThread(self.watchDog, multiprocess=True)
    def watchDog(self, active, eventQueue):
        # echo "command say this is a test" | socat - UNIX-CLIENT:/tmp/fenrirscreenreader-deamon.sock

        if self.env['runtime']['settingsManager'].getSetting('screen', 'driver') =='vcsaDriver':
            socketpath = self.env['runtime']['settingsManager'].getSettingAsInt('remote', 'socketpath') + 'fenrirscreenreader-deamon.sock'
        else:
            socketpath = self.env['runtime']['settingsManager'].getSettingAsInt('remote', 'socketpath') + 'fenrirscreenreader-' + str(os.getpid()) + '.sock'
        if os.path.exists(socketpath):
            os.remove(socketpath)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(socketpath)
        self.sock.listen(1)
        if self.env['runtime']['settingsManager'].getSetting('screen', 'driver') =='vcsaDriver':
            os.chmod(socketpath, 0o222)
        while active.value == 1:
            client_sock, client_addr = self.sock.accept()
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    r, w, e = select.select([client_sock,], [], [])
                except select.error:
                    return
                if len(r) > 0:
                    rawdata = client_sock.recv(8129)
                    try:
                        data = rawdata.decode("utf-8").rstrip().lstrip()
                        eventQueue.put({"Type":fenrirEventType.RemoteIncomming,
                            "Data": data
                        })
                    except:
                        pass
                client_sock.close()

        if os.path.exists(socketpath):
            os.remove(socketpath)
        if self.sock:
            self.sock.close()
            self.sock = None
