#!/bin/python
import dbus
try:
    bus = dbus.SystemBus()
    obj  = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
    inf = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
    ListSessions = inf.get_dbus_method('ListSessions')
    sessions = ListSessions()
    for session in sessions:
        obj = bus.get_object('org.freedesktop.login1', session[4])
        inf = dbus.Interface(obj, 'org.freedesktop.DBus.Properties')
        sessionType = inf.Get('org.freedesktop.login1.Session', 'Type')
        screen = str(inf.Get('org.freedesktop.login1.Session', 'VTNr'))                                                            
        if screen == '':  
            screen = str(inf.Get('org.freedesktop.login1.Session', 'TTY'))
            print('Session:', screen, 'Type:', sessionType.upper(), 'Details:', session)
        else:
            print('Session:', screen, 'Type:', sessionType.upper(), 'Details:', session)
except:
    print('no access')                                                                             
