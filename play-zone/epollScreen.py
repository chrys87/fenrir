#!/bin/python

import select
import time

currScreen = '2'
vcsa = {}
for i in range(1,7):
    vcsa[str(i)] = open('/dev/vcs'+str(i),'rb')

tty = open('/sys/devices/virtual/tty/tty0/active','r')
currScreen = str(tty.read()[3:-1])
oldScreen = currScreen
watchdog = select.epoll()
watchdog.register(vcsa[currScreen], select.EPOLLPRI)
watchdog.register(tty, select.EPOLLPRI)
    
while True:
    changes = watchdog.poll()
    print('-----------------------------')
    print(changes)
    for change in changes:
        fileno = change[0]
        event = change[1]
        print(change,fileno, tty.fileno())
        if fileno == tty.fileno():
            tty.seek(0)
            currScreen = str(tty.read()[3:-1])        
            if currScreen != oldScreen:
                watchdog.unregister(vcsa[ oldScreen ])              
                watchdog.register(vcsa[ currScreen ], select.EPOLLPRI)   
                oldScreen = currScreen  
                print('new screen '+ currScreen)            
        else:
            vcsa[currScreen].seek(0)
            content = vcsa[currScreen].read()
            print('update '+ str(time.time()))
