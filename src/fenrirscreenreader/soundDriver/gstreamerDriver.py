#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time, threading
from fenrirscreenreader.core.soundDriver import soundDriver

_gstreamerAvailable = False
try:
    import gi        
    from gi.repository import GLib        
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
    _gstreamerAvailable, args = Gst.init_check(None)   
except Exception as e:
    _gstreamerAvailable = False
    _availableError = str(e)

class driver(soundDriver):
    def __init__(self):
        soundDriver.__init__(self)
        self._source = None
        self._sink = None
        
    def initialize(self, environment):
        self.env = environment
        global _gstreamerAvailable
        self._initialized = _gstreamerAvailable              
        if not self._initialized:
            global _availableError
            self.environment['runtime']['debug'].writeDebugOut('Gstreamer not available ' + _availableError,debug.debugLevel.ERROR)                        
            return
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
        self.mainloop = GLib.MainLoop()        
        self.thread = threading.Thread(target=self.mainloop.run)
        self.thread.start()

    def shutdown(self):
        if not self._initialized:
            return
        self.cancel()
        self.mainloop.quit()

    def _onPlayerMessage(self, bus, message):
        if not self._initialized:
            return    
        if message.type == Gst.MessageType.EOS:
            self._player.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self._player.set_state(Gst.State.NULL)
            error, info = message.parse_error()
            self.env['runtime']['debug'].writeDebugOut('GSTREAMER: _onPlayerMessage'+ str(error) + str(info),debug.debugLevel.WARNING)                        

    def _onPipelineMessage(self, bus, message):
        if not self._initialized:
            return    
        if message.type == Gst.MessageType.EOS:
            self._pipeline.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self._pipeline.set_state(Gst.State.NULL)
            error, info = message.parse_error()
            self.env['runtime']['debug'].writeDebugOut('GSTREAMER: _onPipelineMessage'+ str(error) + str(info),debug.debugLevel.WARNING)  
            
    def _onTimeout(self, element):
        if not self._initialized:
            return    
        element.set_state(Gst.State.NULL)

    def playSoundFile(self, fileName, interrupt=True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        self._player.set_property('uri', 'file://%s' % fileName)
        self._player.set_state(Gst.State.PLAYING)

    def playFrequence(self, frequence, duration, adjustVolume, interrupt=True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        self._source.set_property('volume', tone.volume)
        self._source.set_property('freq', tone.frequency)
        self._source.set_property('wave', tone.wave)
        self._pipeline.set_state(Gst.State.PLAYING)
        duration = int(1000 * tone.duration)
        GLib.timeout_add(duration, self._onTimeout, self._pipeline)

    def cancel(self, element=None):
        if not self._initialized:
            return
        if element:
            element.set_state(Gst.State.NULL)
            return
        self._player.set_state(Gst.State.NULL)
        self._pipeline.set_state(Gst.State.NULL)
