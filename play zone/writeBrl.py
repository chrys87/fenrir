#!/bin/python

import brlapi
import time

brl = brlapi.Connection()
brl.enterTtyMode()
print('display size' + str(brl.displaySize))
print('driver name'+str(brl.driverName))

t = time.time()
while(time.time() - t <= 5):
    try:
        brl.writeText(0,'this is a 5 second test')
    except Exception as e:
        print(e)
    

