#!/usr/bin/python
import gi        
from gi.repository import GLib        
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import time, threading
gi.require_version('Atspi', '2.0')
import pyatspi

# Callback to print the active window on key press amd filter out the key release
def on_key_input(event):
    print(event)

mainloop = GLib.MainLoop()        
thread = threading.Thread(target=mainloop.run)
thread.start()
#pyatspi.Registry.registerKeystrokeListener(on_key_input, kind=(pyatspi.KEY_PRESSED_EVENT, pyatspi.KEY_RELEASED_EVENT))
pyatspi.Registry.registerKeystrokeListener(on_key_input,mask=pyatspi.allModifiers(), kind=(pyatspi.KEY_PRESS,pyatspi.KEY_RELEASE,pyatspi.KEY_PRESSRELEASE), synchronous=True, preemptive=True)
pyatspi.Registry.start()
