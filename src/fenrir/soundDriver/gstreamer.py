#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import gi
import time, threading
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)

class driver:
    def __init__(self):
        self._initialized = False
        self._source = None
        self._sink = None
        self.volume = 1
    def initialize(self, environment):
        if self._initialized:
           return
        global _gstreamerAvailable           
        if not _gstreamerAvailable:
            self.environment['runtime']['debug'].writeDebugOut('Gstreamer not available',debug.debugLevel.ERROR)                        
            return
        self.env = environment
        self._player = Gst.ElementFactory.make('playbin', 'player')
        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._onPlayerMessage)

        self._pipeline = Gst.Pipeline(name='fenrir-pipeline')
        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._onPipelineMessage)

        self._source = Gst.ElementFactory.make('audiotestsrc', 'src')
        self._sink = Gst.ElementFactory.make('autoaudiosink', 'output')
        self._pipeline.add(self._source)
        self._pipeline.add(self._sink)
        self._source.link(self._sink)

        self._initialized = True
        self.thread = threading.Thread(target=self.main)
        self.thread.start()
    def shutdown(self):
        global _gstreamerAvailable    
        if not _gstreamerAvailable:
            return
        self.cancel()
        Gtk.main_quit()
        self._initialized = False
        _gstreamerAvailable = False

    def _onPlayerMessage(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            self._player.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self._player.set_state(Gst.State.NULL)
            error, info = message.parse_error()
            self.env['runtime']['debug'].writeDebugOut('GSTREAMER: _onPlayerMessage'+ str(error) + str(info),debug.debugLevel.WARNING)                        

    def _onPipelineMessage(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            self._pipeline.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self._pipeline.set_state(Gst.State.NULL)
            error, info = message.parse_error()
            self.env['runtime']['debug'].writeDebugOut('GSTREAMER: _onPipelineMessage'+ str(error) + str(info),debug.debugLevel.WARNING)  
            
    def _onTimeout(self, element):
        element.set_state(Gst.State.NULL)

    def playSoundFile(self, fileName, interrupt=True):
        if interrupt:
            self.cancel()
        self._player.set_property('uri', 'file://%s' % fileName)
        self._player.set_state(Gst.State.PLAYING)

    def playFrequence(self, frequence, duration, adjustVolume, interrupt=True):
        if interrupt:
            self.cancel()
        self._source.set_property('volume', tone.volume)
        self._source.set_property('freq', tone.frequency)
        self._source.set_property('wave', tone.wave)
        self._pipeline.set_state(Gst.State.PLAYING)
        duration = int(1000 * tone.duration)
        GLib.timeout_add(duration, self._onTimeout, self._pipeline)
    def main(self):
        Gtk.main()
    def cancel(self, element=None):
        global _gstreamerAvailable    
        if not _gstreamerAvailable:
            return
        if element:
            element.set_state(Gst.State.NULL)
            return
        self._player.set_state(Gst.State.NULL)
        self._pipeline.set_state(Gst.State.NULL)
    def setVolume(self, volume):
        self.volume = volume  



