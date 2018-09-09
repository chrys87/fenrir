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
        # echo "command say this is a test" | nc localhost 22447
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = '127.0.0.1'
        self.port = self.env['runtime']['settingsManager'].getSettingAsInt('remote', 'port')
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
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
        if self.sock:
            self.sock.close()
            self.sock = None
