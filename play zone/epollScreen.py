#!/bin/python

import select
import time

vcsa = {}
for i in range(1,7):
    vcsa[str(i)] = open('/dev/vcs'+str(i),'rb')
    vcsa[str(i)].read()

tty = open('/sys/devices/virtual/tty/tty0/active','r')

oldTty = str(tty.read()[3:-1])
watchdog = select.poll()
watchdog.register(tty, select.EPOLLPRI)
watchdog.register(vcsa[ oldTty ], select.EPOLLPRI)

while True:
    changed = watchdog.poll()
    print('-----------------------------')
    print(changed,tty.fileno())
    for fileno, event in changed:
        if tty.fileno() == fileno: 
            currTty = tty.seek(0)
            #b = open('/sys/devices/virtual/tty/tty0/active','r')  
            currTty = str(tty.read()[3:-1])
            print('|'+currTty+'|'+oldTty+'|')
            if currTty != oldTty:
                watchdog.register(vcsa[ currTty ].fileno(), select.EPOLLPRI)   
                watchdog.unregister(vcsa[ oldTty ].fileno())  
                oldTty = currTty
                print('new screen ' + currTty)
        else:
            print('update '+ currTty + ' ' + str(fileno))
            vcsa[currTty].seek(0)
            b = vcsa[currTty].read()
            #print(b)
    time.sleep(0.5)



