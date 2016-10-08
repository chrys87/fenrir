#!/bin/python

import brlapi
import time

brl = brlapi.Connection()
print(brl.displaySize)
print(brl.driverName)

t = time.time()
while(time.time() - t <= 5):
    try:
        brl.writeText('this is a 5 second test')
    except Exception as e:
        print(e)
    

